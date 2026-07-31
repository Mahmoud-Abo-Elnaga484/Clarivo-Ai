import os
import warnings
# إخفاء التحذيرات الخاصة بـ Symlinks على ويندوز وتحذيرات الـ Deprecation غير المؤثرة
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore")

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

# تحديد الموديل اللي هيحول النصوص لأرقام (Embeddings)
embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
DB_PATH = "vector_db/faiss_index"

def build_knowledge_base():
    """
    بناء الفيكتور داتا بيز من المناهج وطرق الشرح اللي إحنا محددينها.
    """
    docs = [
        # ---------------- MATH ----------------
        Document(
            page_content="""
            Topic: Fractions (الكسور)
            Goal: Understand that fractions are equal parts of a whole.
            Parent Explanation: Explain to your child by cutting an apple, a small cake, or a pizza into equal slices. Show them that 1 slice out of 4 is 1/4. Use physical objects!
            Common Mistakes: Adding denominators (e.g., 1/2 + 1/2 = 2/4). Emphasize that the bottom number (denominator) is just the "name" of the size of the piece and doesn't get added.
            Daily Activity: Ask the child to divide a chocolate bar equally among family members.
            """,
            metadata={"subject": "Math", "topic": "Fractions", "language": "English", "resource_link": "https://www.khanacademy.org/math/arithmetic/fraction-arithmetic"}
        ),
        Document(
            page_content="""
            Topic: Addition (الجمع البسيط)
            Goal: Understand combining two groups of items into one larger group.
            Parent Explanation: Do not use fingers first. Use physical counters like beans, Lego blocks, or small toys. Count the first group, then the second, then push them together and count all.
            Common Mistakes: Starting to count from 1 again instead of continuing from the larger number. Teach them to put the big number in their head and count forward.
            Daily Activity: Ask the child to count the red cars and blue cars on a street and add them up.
            """,
            metadata={"subject": "Math", "topic": "Addition", "language": "English", "resource_link": "https://www.khanacademy.org/math/arithmetic/arith-review-add-subtract"}
        ),
        Document(
            page_content="""
            Topic: Division (القسمة)
            Goal: Understand how division splits numbers into equal groups.
            Parent Explanation: Explain division using sharing objects equally between people. Example: 8 ÷ 2 means splitting 8 items into 2 equal groups, so each group gets 4.
            Common Mistakes: Confusing division symbols with addition symbols or forgetting that division means equal sharing.
            Daily Activity: Ask the child to divide 8 candies equally between 2 people and count how many each person gets.
            """,
            metadata={"subject": "Math", "topic": "Division", "language": "English", "resource_link": "https://www.khanacademy.org/math/arithmetic/arith-review-multiply-divide"}
        ),

        # ---------------- SCIENCE ----------------
        Document(
            page_content="""
            Topic: Photosynthesis (البناء الضوئي)
            Goal: Understand how plants make their own food using sunlight.
            Parent Explanation: Tell a story: The plant is like a tiny chef. It needs 3 ingredients to cook: Sunlight (fire), Water (from rain), and Air (Carbon Dioxide). It cooks them in its green leaves to make sugar (food) and breathes out Oxygen for us.
            Common Mistakes: Believing plants get their "food" from the soil. Clarify that soil only provides vitamins (minerals), but the plant makes the actual food itself.
            Daily Activity: Put a plant near a window and another in a dark closet for two days, then compare them to see why sunlight is important.
            """,
            metadata={"subject": "Science", "topic": "Photosynthesis", "language": "English", "resource_link": "https://www.khanacademy.org/science/biology/photosynthesis-in-plants"}
        ),
        Document(
            page_content="""
            Topic: Water Cycle (دورة المياه)
            Goal: Learn how water moves around the Earth (Evaporation, Condensation, Precipitation).
            Parent Explanation: Boil water in a pot. Show the steam going up (Evaporation). Put a cold lid over it, show the water drops forming (Condensation), then let them fall back (Precipitation/Rain).
            Common Mistakes: Thinking clouds are made of gas. Clarify that clouds are actually tiny liquid water droplets floating in the air.
            Daily Activity: Leave a small glass of water in the sun and mark the water level. Check it the next day to see evaporation in action.
            """,
            metadata={"subject": "Science", "topic": "Water Cycle", "language": "English", "resource_link": "https://www.khanacademy.org/science/biology/ecology/biogeochemical-cycles"}
        ),

        # ---------------- ARABIC ----------------
        Document(
            page_content="""
            Topic: الجملة الاسمية (Nominal Sentence)
            Goal: أن يفهم الطفل أن الجملة الاسمية تبدأ باسم وتتكون من مبتدأ وخبر.
            Parent Explanation: العب مع طفلك لعبة "صاحب البيت والضيف". المبتدأ هو صاحب البيت (الاسم الأول)، والخبر هو الضيف اللي بيجي يكمل المعنى ويجيب الأخبار. زي "الشمسُ (صاحب البيت) ساطعةٌ (الضيف)".
            Common Mistakes: الخلط بين المبتدأ والفعل. دايماً خلي الطفل يجرب يحط (الـ) في أول الكلمة، لو نفعت يبقى اسم (مبتدأ).
            Daily Activity: اطلب من الطفل يوصف أوضته بـ 3 جمل تبدأ باسم (مثال: السريرُ مرتبٌ، اللعبةُ جميلةٌ).
            """,
            metadata={"subject": "Arabic", "topic": "الجملة الاسمية", "language": "Arabic", "resource_link": "https://www.khanacademy.org/international/ar"}
        ),

        # ---------------- ENGLISH ----------------
        Document(
            page_content="""
            Topic: Present Simple (المضارع البسيط)
            Goal: Understand that we use Present Simple for habits and facts.
            Parent Explanation: Explain it as "The Routine Tense". Ask the child about what they do every single day. Emphasize the "Superman S": He, She, and It always need the "S" at the end of the verb (He plays, She eats).
            Common Mistakes: Using "verb+ing" for habits (e.g., saying "I am going to school everyday" instead of "I go").
            Daily Activity: Ask the child to describe the daily morning routine of their pet or favorite superhero.
            """,
            metadata={"subject": "English", "topic": "Present Simple", "language": "English", "resource_link": "https://www.khanacademy.org/ela"}
        )
    ]

    print("Building FAISS Knowledge Base with new subjects...")
    vectorstore = FAISS.from_documents(docs, embedding_model)
    vectorstore.save_local(DB_PATH)
    print("Knowledge Base saved successfully!")


def get_context(topic_name: str, language: str = None) -> str:
    """
    يستقبل اسم الدرس ولغة الواجب، وبيدور على أقرب خطة شرح بنفس اللغة.
    لو مفيش مستند بنفس اللغة قريب بشكل كافي، بيرجع "مفيش context" بدل ما يجيب
    مستند بلغة تانية يلخبط الموديل (زي مستند عربي لواجب إنجليزي أو العكس).
    """
    if not os.path.exists(DB_PATH):
        build_knowledge_base()

    vectorstore = FAISS.load_local(DB_PATH, embedding_model, allow_dangerous_deserialization=True)

    # بنجيب أكتر من نتيجة عشان نقدر نفلتر باللغة من بينهم
    results_with_scores = vectorstore.similarity_search_with_score(topic_name, k=5)

    if not results_with_scores:
        return "No specific teaching context found for this topic. Use general teaching guidelines to help the parent."

    if language:
        filtered = [
            (doc, score) for doc, score in results_with_scores
            if doc.metadata.get("language") == language
        ]
    else:
        filtered = results_with_scores

    if not filtered:
        return "No specific teaching context found for this topic. Use general teaching guidelines to help the parent."

    best_doc, _ = filtered[0]
    return best_doc.page_content


def get_resource_link(topic_name: str, language: str = None) -> str:
    """
    بترجع لينك تعليمي حقيقي وموثوق مرتبط بالموضوع، من قاعدة المعرفة بتاعتنا
    (مش من توليد الـ LLM، عشان نتجنب لينكات وهمية أو غير موجودة).
    """
    if not os.path.exists(DB_PATH):
        build_knowledge_base()

    vectorstore = FAISS.load_local(DB_PATH, embedding_model, allow_dangerous_deserialization=True)
    results_with_scores = vectorstore.similarity_search_with_score(topic_name, k=5)

    if not results_with_scores:
        return ""

    if language:
        filtered = [
            (doc, score) for doc, score in results_with_scores
            if doc.metadata.get("language") == language
        ]
    else:
        filtered = results_with_scores

    if not filtered:
        return ""

    best_doc, _ = filtered[0]
    return best_doc.metadata.get("resource_link", "")


# سطر إضافي عشان لو حبيت تبني الداتا بيز يدوياً بإنك تشغل الفايل ده مباشرة
if __name__ == "__main__":
    build_knowledge_base()