"""
@Time: 2025-03-03
@Auth: Adam Lyu
"""
from langdetect import detect

# (local ?)



def detect_language_langdetect(text):
    """
    Detects the language of the input text using langdetect, returning 'fr' or 'en'.
    Args:
        text (str): The text input by the student
    Returns:
        str: The detected language ('fr' or 'en')
    """
    detected_lang = detect(text)
    if detected_lang.startswith('fr'):
        return 'fr'
    elif detected_lang.startswith('en'):
        return 'en'
    else:
        return 'en'  # Default to English

# Example usage
def process_with_clu(text, language):
    """
    Simulates processing with CLU using the detected language.
    Args:
        text (str): The input text
        language (str): The detected language
    Returns:
        dict: A sample result dictionary
    """
    print(f"CLU processing - Text: {text}, Language: {language}")
    return {"result": f"Processed with {language}"}

# Test cases
if __name__ == "__main__":
    text1 = "Bonjour, comment vas-tu?"
    text2 = "Hello, how are you?"
    lang1 = detect_language_langdetect(text1)
    lang2 = detect_language_langdetect(text2)
    print(process_with_clu(text1, lang1))  # Output: {'result': 'Processed with fr'}
    print(process_with_clu(text2, lang2))  # Output: {'result': 'Processed with en'}