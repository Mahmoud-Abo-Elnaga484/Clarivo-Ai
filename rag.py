import re
import json

from json_repair import repair_json
from retriever import get_context, get_resource_link
from prompts import plan_prompt
from parser import parser, HomeworkPlan
from llm import call_local_llm


def _strip_cjk_characters(text: str) -> str:
    """
    بتشيل أي حروف صينية/يابانية/كورية ممكن الموديل يسربها بالغلط
    (مشكلة معروفة في الموديلات المكمّاة زي Qwen في الردود الطويلة).
    """
    cjk_pattern = re.compile(
        r"[\u4e00-\u9fff\u3400-\u4dbf\u3000-\u303f\u3040-\u30ff\uac00-\ud7af\uff00-\uffef]+"
    )
    return cjk_pattern.sub("", text)


def _flatten_to_text(value) -> str:
   
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        parts = []
        for k, v in value.items():
            label = str(k).replace("_", " ").strip().capitalize()
            parts.append(f"{label}: {_flatten_to_text(v)}")
        return "\n".join(parts)
    if isinstance(value, list):
        return "\n".join(_flatten_to_text(v) for v in value)
    return str(value)


def _flatten_to_string_list(value) -> list:
    
    if value is None:
        return []
    if isinstance(value, list):
        result = []
        for item in value:
            if isinstance(item, str):
                result.append(item)
            else:
                result.append(_flatten_to_text(item))
        return result
    if isinstance(value, str):
        return [value]
    return [_flatten_to_text(value)]


_KEY_ALIASES = {
    "lesson": "lesson",
    "goal": "goal",
    "objective": "goal",
    "parentexplanation": "parent_explanation",
    "parentexplanations": "parent_explanation",
    "explanation": "parent_explanation",
    "howtoexplain": "parent_explanation",
    "commonmistakes": "common_mistakes",
    "mistakes": "common_mistakes",
    "dailyactivity": "daily_activity",
    "activity": "daily_activity",
    "practicequestions": "practice_questions",
    "answers": "answers",
    "difficulty": "difficulty",
    "estimatedtime": "estimated_time",
    "time": "estimated_time",
}


def _normalize_plan_dict(raw_data: dict, questions: list) -> dict:
    """
    بتاخد أي JSON رجعه الموديل (حتى لو أسماء المفاتيح غلط أو الهيكل متداخل)
    وتحوله لنفس شكل HomeworkPlan بالظبط، بدل ما نرفضه كله ونروح للـ fallback.
    """
    normalized = {}

    for raw_key, value in raw_data.items():
        clean_key = re.sub(r"[^a-z]", "", raw_key.lower())
        mapped_key = _KEY_ALIASES.get(clean_key)
        if mapped_key:
            normalized[mapped_key] = value

    fixed = {
        "lesson": _flatten_to_text(normalized.get("lesson", "Unknown")) or "Unknown",
        "goal": _flatten_to_text(normalized.get("goal", "")) or "",
        "parent_explanation": _flatten_to_text(normalized.get("parent_explanation", "")),
        "common_mistakes": _flatten_to_string_list(normalized.get("common_mistakes", [])),
        "daily_activity": _flatten_to_text(normalized.get("daily_activity", "")),
        "practice_questions": _flatten_to_string_list(normalized.get("practice_questions", [])),
        "difficulty": _flatten_to_text(normalized.get("difficulty", "Unknown")) or "Unknown",
        "estimated_time": _flatten_to_text(normalized.get("estimated_time", "Unknown")) or "Unknown",
    }

    raw_answers = normalized.get("answers", [])
    fixed_answers = []
    if isinstance(raw_answers, list):
        for item in raw_answers:
            if isinstance(item, dict):
                fixed_answers.append({
                    "question": _flatten_to_text(item.get("question", "")),
                    "answer": _flatten_to_text(item.get("answer", "")),
                    "explanation": _flatten_to_text(item.get("explanation", "")),
                })
    if len(fixed_answers) < len(questions):
        for q in questions[len(fixed_answers):]:
            fixed_answers.append({"question": q, "answer": "", "explanation": ""})
    fixed["answers"] = fixed_answers

    return fixed


def _parse_json_from_text(text: str) -> dict:
    """
    بتستخرج الـ JSON من النص حتى لو ملفوف في ```json ... ``` أو ``` ... ```.
    """
    pattern = r"```(?:json)?\s*\n?(.*?)\n?\s*```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        text = match.group(1).strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
    
        repaired = repair_json(text)
        return json.loads(repaired)


def generate_teaching_plan(extracted_info: dict, material_context: str = None) -> dict:
    """
    بتاخد البيانات المستخرجة من الصورة (من Gemini Vision)، بتجيب السياق من
    قاعدة المعرفة (والمنهج اللي اليوزر رفعه لو موجود)، وبتولد خطة الشرح +
    إجابة كل سؤال باستخدام Qwen (Kaggle).
    """
    topic = extracted_info.get("topic", "Unknown")
    questions = extracted_info.get("questions", [])
    language = extracted_info.get("language", "English")

    # بنبعت اللغة لـ get_context عشان يفلتر ومايجيبش context بلغة مختلفة
    context_text = get_context(topic, language=language)

    # لينك حقيقي من قاعدة المعرفة (مش من توليد الموديل)
    resource_link = get_resource_link(topic, language=language)

    strict_instruction = (
        """
        جاوب على كل الأسئلة المستخرجة واحد واحد، بعد الانتهاء من شرح الدرس.
        استخدم العربية فقط في كل أجزاء الرد.
        ممنوع استخدام أي كلمات إنجليزية إلا لو موجودة في السؤال نفسه.
        أضف شرحاً بسيطاً بعد كل إجابة.
        لا تتجاهل أي سؤال.
        """
        if language == "Arabic"
        else
        """
        Answer ALL extracted questions one by one, AFTER finishing the teaching explanation.
        Use English only in the entire response.
        Add a short explanation after each answer.
        Never skip any question.
        """
    )

    prompt_value = plan_prompt.format(
        subject=extracted_info.get("subject", "Unknown"),
        topic=topic,
        grade_level=extracted_info.get("grade_level", "Unknown"),
        questions=questions,
        context=context_text,
        language=language,
        material_context=material_context or "No course material was provided by the parent for this topic.",
    )

    material_priority_note = (
        """
        - لديك مادة منهج حقيقية رفعها ولي الأمر (قسم "Reference Material from Uploaded Course Book" فوق).
          استخدمها كـ **المصدر الأساسي والأوثق** لبناء الشرح والإجابات، وقلل الاعتماد على معرفتك
          العامة قدر الإمكان. لو المادة المرفوعة مالهاش علاقة بالسؤال، وضح ده واستخدم معرفتك العامة كبديل.
        """
        if material_context
        else ""
    )

    prompt_value += f"""

IMPORTANT RULES:
- DETECTED HOMEWORK LANGUAGE: {language}. Your ENTIRE response must be written in {language} only, with no exceptions.
- NEVER output any Chinese, Japanese, or Korean characters under any circumstances.
- {strict_instruction}
{material_priority_note}
- Put the 'answers' section AFTER the teaching explanation is fully generated, not before.
- If the homework contains arithmetic operations, solve them carefully step-by-step.
- Double-check multiplication and division results before answering.
- Keep equations exactly as written in the homework.
- The number of answers in 'answers' MUST equal the number of extracted questions.
- Every answer must include:
  1. question
  2. answer
  3. explanation
- Never skip any question.
- Never mix Arabic and English.
"""

    print("\n[Info] Sending Request to Qwen (Kaggle) to generate plan...")

    try:
        estimated_tokens = 1024

        content_text = call_local_llm(prompt_value, max_new_tokens=estimated_tokens, temperature=0.2)
        content_text = _strip_cjk_characters(content_text)
        print(f"[Debug] Response content preview: {content_text[:200]}...")

        try:
            parsed_plan = parser.parse(content_text)
            result = parsed_plan.model_dump()
            result["resource_link"] = resource_link
            return result
        except Exception as parse_err:
            print(f"[Warning] PydanticOutputParser failed: {parse_err}")
            print("[Info] Trying manual JSON extraction...")

        try:
            raw_data = _parse_json_from_text(content_text)
            normalized_data = _normalize_plan_dict(raw_data, questions)
            parsed_plan = HomeworkPlan(**normalized_data)
            result = parsed_plan.model_dump()
            result["resource_link"] = resource_link
            return result
        except Exception as json_err:
            print(f"[Warning] Manual JSON parsing/normalization also failed: {json_err}")

        print("[Fallback] Returning raw text response.")

        fallback_answers = []
        for question in questions:
            fallback_answers.append({
                "question": question,
                "answer": content_text[:300],
                "explanation": content_text[:500]
            })

        return {
            "lesson": topic,
            "goal": "Could not parse structured plan",
            "parent_explanation": content_text,
            "common_mistakes": [],
            "daily_activity": "",
            "practice_questions": [],
            "answers": fallback_answers,
            "difficulty": "Unknown",
            "estimated_time": "Unknown",
            "resource_link": resource_link
        }

    except Exception as e:
        print(f"Error during RAG generation: {e}")
        return None
