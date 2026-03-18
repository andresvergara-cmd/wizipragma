"""
Module: Identity Validator
Validates and filters agent responses to ensure correct identity (Comfi/Comfama/Colombia)
"""

import re
from loguru import logger


# Palabras prohibidas que indican identidad incorrecta
FORBIDDEN_WORDS = [
    'carlos',
    'méxico',
    'mexico',
    'mxn',
    'centli',
    'cinteotl',
    'azteca',
    'mexicano',
    'mexicana'
]

# Palabras correctas que deben estar presentes
CORRECT_IDENTITY = [
    'comfi',
    'comfama',
    'colombia',
    'colombiano',
    'antioquia',
    'cop'
]


def contains_forbidden_identity(text: str) -> tuple[bool, list[str]]:
    """
    Check if text contains forbidden identity words
    
    Args:
        text: Text to check
        
    Returns:
        tuple: (has_forbidden, list_of_found_words)
    """
    text_lower = text.lower()
    found_words = []
    
    for word in FORBIDDEN_WORDS:
        # Use word boundaries to avoid false positives
        pattern = r'\b' + re.escape(word) + r'\b'
        if re.search(pattern, text_lower):
            found_words.append(word)
    
    return len(found_words) > 0, found_words


def validate_response(response: str) -> dict:
    """
    Validate agent response for correct identity
    
    Args:
        response: Agent response text
        
    Returns:
        dict: Validation result with status and details
    """
    has_forbidden, forbidden_words = contains_forbidden_identity(response)
    
    if has_forbidden:
        logger.warning(f"⚠️ IDENTITY VIOLATION DETECTED: Found forbidden words: {forbidden_words}")
        logger.warning(f"Response preview: {response[:200]}...")
        
        return {
            "valid": False,
            "forbidden_words": forbidden_words,
            "message": "Response contains incorrect identity references"
        }
    
    return {
        "valid": True,
        "message": "Response identity is correct"
    }


def clean_response(response: str) -> str:
    """
    Clean response by removing sentences with forbidden identity
    
    Args:
        response: Original response
        
    Returns:
        str: Cleaned response
    """
    # Split into sentences
    sentences = re.split(r'([.!?]\s+)', response)
    
    cleaned_sentences = []
    removed_count = 0
    
    for i in range(0, len(sentences), 2):
        sentence = sentences[i]
        separator = sentences[i+1] if i+1 < len(sentences) else ''
        
        has_forbidden, words = contains_forbidden_identity(sentence)
        
        if not has_forbidden:
            cleaned_sentences.append(sentence + separator)
        else:
            removed_count += 1
            logger.info(f"Removed sentence with forbidden words {words}: {sentence[:100]}...")
    
    cleaned = ''.join(cleaned_sentences).strip()
    
    if removed_count > 0:
        logger.info(f"✅ Cleaned response: Removed {removed_count} sentences with incorrect identity")
    
    return cleaned


def get_fallback_response(question: str) -> str:
    """
    Get a safe fallback response when identity violation is detected
    
    Args:
        question: User's question
        
    Returns:
        str: Safe fallback response
    """
    return f"""¡Hola! Soy Comfi, tu asistente de Comfama en Colombia. 

Entiendo que preguntas sobre: "{question}"

Déjame ayudarte con información actualizada de Comfama. ¿Podrías reformular tu pregunta o ser más específico sobre lo que necesitas?"""


def validate_and_clean_response(response: str, user_question: str = "") -> str:
    """
    Main function: Validate and clean response
    
    Args:
        response: Agent response
        user_question: Original user question (for fallback)
        
    Returns:
        str: Validated and cleaned response
    """
    validation = validate_response(response)
    
    if not validation["valid"]:
        logger.error(f"🚨 IDENTITY VIOLATION: {validation['forbidden_words']}")
        
        # Try to clean the response
        cleaned = clean_response(response)
        
        # If cleaned response is too short or still has issues, use fallback
        if len(cleaned) < 50 or not validate_response(cleaned)["valid"]:
            logger.warning("Cleaned response too short or still invalid, using fallback")
            return get_fallback_response(user_question)
        
        return cleaned
    
    return response
