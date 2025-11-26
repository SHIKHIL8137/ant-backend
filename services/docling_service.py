from docling.document_converter import DocumentConverter

converter = DocumentConverter()

def extract_text_from_doc(path: str):
    doc = converter.convert(path).document
    return doc.export_to_markdown()
