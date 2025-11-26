import os
import json
import google.generativeai as genai
from core.logger import logger
from services.pii_sanitizer import sanitize_resume_text


def call_gemini_api(text: str) -> dict:
    """
    Call Google Gemini API to parse resume data with privacy protection.
    
    Args:
        text (str): Raw resume text (should be pre-sanitized)
        
    Returns:
        dict: Parsed resume data from Gemini
    """
    # Get API key from environment variable
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise Exception("GEMINI_API_KEY not found in environment variables")
    
    # Configure the Gemini API
    genai.configure(api_key=api_key)
    
    logger.info("Using Google Gemini API")
    
    # Sanitize the text to remove PII
    sanitized_text = sanitize_resume_text(text)
    
    # Secure prompt that ensures privacy
    prompt = f"""
You are a secure and privacy-focused resume parser.

The following resume text has been PRE-CLEANED to REMOVE all personally
identifiable information (PII) such as: name, email, phone number, 
address, LinkedIn, GitHub, portfolio links, and any other user identifiers.

Do NOT try to infer or guess personal details.

Your job is to extract ONLY professional and skill-based information 
from this sanitized text and return it in STRICT JSON format.

Expected JSON structure:

{{
  "skills": {{}},
  "experience": [],
  "professional_projects": [],
  "additional_projects": [],
  "education": [],
  "achievements": [],
  "languages": {{}}
}}

Sanitized Resume Text (PII Removed):
{sanitized_text}

Rules:
- Do NOT add name, contact, or any personal information.
- Do NOT hallucinate details that are not in the text.
- Return ONLY valid JSON response with no additional text or markdown formatting.
- If you cannot extract certain fields, leave them empty but maintain the structure.
- Always return valid JSON, even if empty.
"""

    try:
        # Initialize the Gemini model
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        
        # Generate content with specific generation config
        generation_config = {
            "temperature": 0.2,
            "top_p": 0.95,
            "top_k": 30,
            "max_output_tokens": 8192,
        }
        
        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )
        
        # Log the raw response for debugging
        logger.info(f"Raw Gemini response: {response.text[:200]}...")
        
        # Clean the response text to ensure it's valid JSON
        response_text = response.text.strip()
        
        # Remove any markdown code block markers if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        
        response_text = response_text.strip()
        
        # Parse the JSON response
        parsed_data = json.loads(response_text)
        
        logger.info("Successfully parsed resume data with Gemini API")
        return parsed_data
        
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing Gemini response: {str(e)}")
        logger.error(f"Raw response that failed to parse: {response.text}")
        raise Exception(f"Failed to parse Gemini response: {str(e)}")
    except Exception as e:
        logger.error(f"Error calling Gemini API: {str(e)}")
        raise Exception(f"Failed to call Gemini API: {str(e)}")


# Keep the old function name for backward compatibility
def call_local_llm(text: str) -> dict:
    """
    Call local LLM to parse resume data with privacy protection.
    Now uses Google Gemini API.
    """
    return call_gemini_api(text)