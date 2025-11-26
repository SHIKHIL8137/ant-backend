from fastapi import APIRouter, UploadFile, File
import tempfile
import os
from services.docling_service import extract_text_from_doc
from services.llm_service import call_llm_api
from services.redis_service import redis_service
from core.logger import logger

router = APIRouter()

@router.post("/extract-resume")
async def extract_resume(file: UploadFile = File(...)):
    logger.info(f"Received resume extraction request for file: {file.filename}")
    suffix = os.path.splitext(file.filename)[1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        path = tmp.name

    try:
        logger.info(f"Processing file: {file.filename}")
        raw_text = extract_text_from_doc(path)
        logger.info(f"Successfully extracted text from: {file.filename}")
        
        # Call the configured LLM API to parse the resume data with privacy protection
        llm_parsed_data = call_llm_api(raw_text)
        
        # Create a session and store the parsed data in Redis
        session_id = redis_service.create_session(llm_parsed_data)
        
        logger.info(f"Successfully parsed resume and created session with ID: {session_id}")

        return {
            "status": True,
            "session_id": session_id,
            "professional_data": llm_parsed_data
        }

    except Exception as e:
        logger.error(f"Error processing file {file.filename}: {str(e)}")
        raise

    finally:
        if os.path.exists(path):
            os.remove(path)
            logger.debug(f"Cleaned up temporary file: {path}")