import fitz
# import pdfplumber

def is_text_extractable(text: str) -> bool:
    """
    Determine if PDF contains usable text.
    """

    return len(text.strip()) > 50

# def extract_pdf_text(pdf_path: str) -> str:

#     text = ""

#     try:
#         doc = fitz.open(pdf_path)

#         for page in doc:
#             text += page.get_text()

#         doc.close()

#         if text.strip():
#             return text

#     except Exception:
#         pass

#     try:
#         with pdfplumber.open(pdf_path) as pdf:

#             for page in pdf.pages:
#                 text += page.extract_text() or ""

#         return text.strip()

#     except Exception as e:
#         print(f"Fallback Extraction Error: {e}")
#         return ""


def extract_pdf_text(pdf_path: str) -> str:
    """
    Extract text from PDF using PyMuPDF.
    """

    text = ""

    try:
        doc = fitz.open(pdf_path)

        for page in doc:
            text += page.get_text()

        doc.close()

        return text.strip()

    except Exception as e:
        print(f"PDF Extraction Error: {e}")
        return ""