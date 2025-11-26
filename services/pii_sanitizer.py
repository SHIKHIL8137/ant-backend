import re


def sanitize_resume_text(text: str) -> str:
    """
    Remove personally identifiable information (PII) from resume text.
    
    Args:
        text (str): Raw resume text
        
    Returns:
        str: Sanitized text with PII removed
    """
    # Make a copy of the text to avoid modifying the original
    sanitized_text = text
    
    # Remove email addresses
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    sanitized_text = re.sub(email_pattern, '[EMAIL REMOVED]', sanitized_text)
    
    # Remove phone numbers (various formats)
    phone_patterns = [
        r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',  # 123-456-7890 or 123.456.7890 or 1234567890
        r'\(\d{3}\)\s*\d{3}[-.]?\d{4}',    # (123) 456-7890 or (123)456-7890
        r'\+\d{1,3}\s*\d{3,4}\s*\d{3,4}\s*\d{3,4}',  # +1 123 456 7890
        r'\b\d{3}\s\d{3}\s\d{4}\b'         # 123 456 7890
    ]
    
    for pattern in phone_patterns:
        sanitized_text = re.sub(pattern, '[PHONE REMOVED]', sanitized_text)
    
    # Remove addresses (simple pattern)
    # This is a basic pattern and might need refinement based on specific needs
    address_pattern = r'\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr|Court|Ct|Place|Pl|Square|Sq|Terrace|Ter|Circle|Cir|Parkway|Pkwy|Highway|Hwy)\.?\s*[A-Za-z\s,]*\d{5}(?:-\d{4})?'
    sanitized_text = re.sub(address_pattern, '[ADDRESS REMOVED]', sanitized_text, flags=re.IGNORECASE)
    
    # Remove social media links/profiles
    social_media_patterns = [
        r'(?:https?://)?(?:www\.)?(?:linkedin\.com/[^\s]*)',
        r'(?:https?://)?(?:www\.)?(?:github\.com/[^\s]*)',
        r'(?:https?://)?(?:www\.)?(?:twitter\.com/[^\s]*)',
        r'(?:https?://)?(?:www\.)?(?:facebook\.com/[^\s]*)',
        r'(?:https?://)?(?:www\.)?(?:instagram\.com/[^\s]*)',
        r'(?:https?://)?(?:www\.)?(?:portfolio\.[^\s]*)'
    ]
    
    for pattern in social_media_patterns:
        sanitized_text = re.sub(pattern, '[SOCIAL MEDIA LINK REMOVED]', sanitized_text, flags=re.IGNORECASE)
    
    # Remove names (this is tricky and might need refinement)
    # For now, we'll remove lines that look like names at the beginning of the resume
    lines = sanitized_text.split('\n')
    if lines:
        first_line = lines[0].strip()
        # If the first line looks like a name (no numbers, not too long)
        if first_line and not re.search(r'\d', first_line) and len(first_line.split()) <= 4:
            lines[0] = '[NAME REMOVED]'
            sanitized_text = '\n'.join(lines)
    
    return sanitized_text


def contains_pii(text: str) -> bool:
    """
    Check if text contains personally identifiable information.
    
    Args:
        text (str): Text to check
        
    Returns:
        bool: True if PII is detected, False otherwise
    """
    # Check for email addresses
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.search(email_pattern, text):
        return True
    
    # Check for phone numbers
    phone_patterns = [
        r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
        r'\(\d{3}\)\s*\d{3}[-.]?\d{4}',
        r'\+\d{1,3}\s*\d{3,4}\s*\d{3,4}\s*\d{3,4}',
        r'\b\d{3}\s\d{3}\s\d{4}\b'
    ]
    
    for pattern in phone_patterns:
        if re.search(pattern, text):
            return True
    
    return False