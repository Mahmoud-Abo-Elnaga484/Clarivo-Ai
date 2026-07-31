import io
from PyPDF2 import PdfReader
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from retriever import embedding_model


def extract_text_from_material_pdf(file_bytes: bytes, max_pages: int = 200) -> str:
    """
    بتستخرج النص الحقيقي من PDF منهج/كتاب دراسي (مش صورة واجب ممسوحة).
    الكتب الدراسية غالباً PDF نصي حقيقي، فـ PyPDF2 هنا مناسبة تماماً
    (على عكس صور الواجبات الممسوحة ضوئياً اللي بنستخدملها pypdfium2 + Gemini Vision).
    """
    reader = PdfReader(io.BytesIO(file_bytes))
    texts = []

    page_count = min(len(reader.pages), max_pages)
    for i in range(page_count):
        page_text = reader.pages[i].extract_text() or ""
        if page_text.strip():
            texts.append(page_text.strip())

    return "\n\n".join(texts)


def _chunk_text(text: str, chunk_size: int = 900, overlap: int = 150) -> list:
    """
    بتقسم النص لأجزاء صغيرة متداخلة شوية (overlap) عشان محتوى مهم مايتقطعش
    في نص جزئين، وعشان البحث الدلالي يشتغل صح على أجزاء بحجم معقول.
    """
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == text_length:
            break
        start = end - overlap

    return chunks


def build_material_vectorstore(material_text: str):
    """
    بتبني فهرس FAISS في الذاكرة بس (من غير حفظ على القرص)، عشان كل مستخدم
    عنده منهجه الخاص وده بيتغير من رفعة لرفعة - مش قاعدة معرفة ثابتة.
    """
    if not material_text or not material_text.strip():
        return None

    chunks = _chunk_text(material_text)
    if not chunks:
        return None

    docs = [Document(page_content=chunk) for chunk in chunks]
    vectorstore = FAISS.from_documents(docs, embedding_model)
    return vectorstore


def get_material_context(vectorstore, query: str, k: int = 3) -> str:
    """
    بتدور جوه فهرس المنهج المرفوع عن أقرب الأجزاء لموضوع/أسئلة الواجب،
    وبترجعهم كنص واحد يتحط في الـ prompt كمصدر أساسي موثوق.
    """
    if vectorstore is None or not query:
        return ""

    results = vectorstore.similarity_search(query, k=k)
    if not results:
        return ""

    return "\n\n---\n\n".join(doc.page_content for doc in results)