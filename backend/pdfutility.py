def extract_text_from_pdf(pdf_bytes):
    from PyPDF2 import PdfReader
    import io
    reader = PdfReader(io.BytesIO(pdf_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text