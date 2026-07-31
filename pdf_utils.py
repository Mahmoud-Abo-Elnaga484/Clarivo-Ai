import pypdfium2 as pdfium
from PIL import Image


def pdf_to_images(file_bytes: bytes, dpi: int = 200, max_pages: int = 15) -> list:
    """
    بتحول كل صفحة في ملف PDF لصورة PIL.Image، عشان نقدر نبعتها لـ Gemini Vision
    بنفس الطريقة اللي بنبعت بيها صورة عادية. باستخدام pypdfium2 (خفيفة ومفيهاش
    أي متطلبات خارجية زي poppler).
    max_pages بيحدد أقصى عدد صفحات نقراها (حماية من ملفات كبيرة جداً).
    """
    images = []
    scale = dpi / 72  # pypdfium2 بيشتغل بـ scale factor مش DPI مباشرة

    pdf = pdfium.PdfDocument(file_bytes)
    try:
        page_count = min(len(pdf), max_pages)
        for page_index in range(page_count):
            page = pdf[page_index]
            bitmap = page.render(scale=scale)
            pil_image = bitmap.to_pil().convert("RGB")
            images.append(pil_image)
            page.close()
    finally:
        pdf.close()

    return images