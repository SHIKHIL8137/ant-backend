from fastapi import APIRouter, UploadFile, File
import tempfile
import os
from services.docling_service import extract_text_from_doc
from core.logger import logger

router = APIRouter()

@router.post("/extract-resume")
async def extract_resume(file: UploadFile = File(...)):
    suffix = os.path.splitext(file.filename)[1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        path = tmp.name

    try:
        text = extract_text_from_doc(path)

        return {
            "status": True,
            "text": text
        }

    finally:
        if os.path.exists(path):
            os.remove(path)
