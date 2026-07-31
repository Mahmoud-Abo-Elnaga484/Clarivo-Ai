import os
import re
import json
import base64
from io import BytesIO
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from PIL import Image

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")


def pil_to_base64(image: Image.Image) -> str:
    """تحويل الصورة إلى صيغة Base64 عشان LangChain يقدر يقرأها"""
    buffered = BytesIO()
    if image.mode != 'RGB':
        image = image.convert('RGB')
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


def detect_language(text: str) -> str:
    """
    تحديد لغة الواجب اعتماداً على وجود حروف عربية في النص.
    بنستخدمها كمصدر موثوق للغة بدل ما نصدق الموديل، لأنه بيغلط أحياناً.
    """
    arabic_chars = re.findall(r"[\u0600-\u06FF]", text or "")
    return "Arabic" if arabic_chars else "English"


def extract_homework_details(image: Image.Image) -> dict:
    """
    بتاخد صورة واحدة وتستخرج منها subject/topic/grade_level/questions/language
    باستخدام Gemini Vision.
    """
    if not google_api_key:
        print("Error: GOOGLE_API_KEY is missing!")
        return {
            "subject": "Error", "grade_level": "Error",
            "topic": "Missing API Key", "questions": [], "language": "English",
        }

    llm = ChatGoogleGenerativeAI(
        model="gemini-flash-latest",
        temperature=0.1,
        max_retries=2,
        api_key=google_api_key,
    )

    prompt_text = """
    Analyze the uploaded homework image and extract the following information.
    You MUST return the response strictly in valid JSON format with exactly these keys:
    - "subject": The main subject of the homework.
    - "grade_level": Guess the grade level if possible.
    - "topic": The specific lesson or topic.
    - "questions": A list of strings, where each string is a single question extracted, kept
      in the SAME language as it appears in the image (do not translate the questions).
    - "language": Either "Arabic" or "English", matching the dominant language of the homework.

    Extract EVERY question found in the image, do not stop early even if there are many.
    If the image has no visible homework questions, return an empty "questions" list.

    Return ONLY the JSON. Do not include markdown blocks like ```json ... ``` or any other text.
    """

    img_base64 = pil_to_base64(image)
    message = HumanMessage(
        content=[
            {"type": "text", "text": prompt_text},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}}
        ]
    )

    try:
        response = llm.invoke([message])
        content = response.content

        if isinstance(content, list):
            response_text = ""
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    response_text += block.get("text", "")
                elif isinstance(block, str):
                    response_text += block
        else:
            response_text = str(content)

        response_text = response_text.strip()
        if response_text.startswith("```json"):
            response_text = response_text.replace("```json", "").replace("```", "").strip()
        elif response_text.startswith("```"):
            response_text = response_text.replace("```", "").strip()

        extracted_data = json.loads(response_text)

        # مهم: منسيبش الموديل يقرر قيمة "language" بمفرده، بنستنتجها من النص الفعلي
        questions_text = " ".join(extracted_data.get("questions", []))
        extracted_data["language"] = detect_language(questions_text)

        return extracted_data

    except Exception as e:
        print(f"\n--- Error during extraction --- \n{e}\n---------------------------\n")
        return {
            "subject": "Unknown", "grade_level": "Unknown",
            "topic": "Unknown", "questions": [], "language": "English",
        }


def extract_homework_details_from_pages(images: list) -> dict:
    """
    بتاخد قائمة صور (صفحات PDF مثلاً)، بتستخرج من كل صفحة على حدة، وبتدمج
    النتايج كلها في نتيجة واحدة (subject/topic/grade_level من أول صفحة فيها بيانات،
    والأسئلة من كل الصفحات مجمعة).
    """
    combined = {
        "subject": "Unknown", "grade_level": "Unknown",
        "topic": "Unknown", "questions": [], "language": "English",
    }

    for page_image in images:
        page_data = extract_homework_details(page_image)

        if combined["subject"] == "Unknown" and page_data.get("subject", "Unknown") != "Unknown":
            combined["subject"] = page_data.get("subject", "Unknown")
        if combined["topic"] == "Unknown" and page_data.get("topic", "Unknown") != "Unknown":
            combined["topic"] = page_data.get("topic", "Unknown")
        if combined["grade_level"] == "Unknown" and page_data.get("grade_level", "Unknown") != "Unknown":
            combined["grade_level"] = page_data.get("grade_level", "Unknown")

        combined["questions"].extend(page_data.get("questions", []))

    combined["language"] = detect_language(" ".join(combined["questions"]))
    return combined