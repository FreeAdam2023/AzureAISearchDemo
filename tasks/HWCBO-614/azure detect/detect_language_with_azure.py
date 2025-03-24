"""
@Time: 2025-03-03
@Auth: Adam Lyu
"""
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# Azure Text Analytics configuration
TA_ENDPOINT = "https://demolyulanguageservice-v2.cognitiveservices.azure.com/"
TA_KEY = "7wx94XIiJNNtz4cZIob3O10Q0GEIo46k3Oa3455PiWzEFEFgty28JQQJ99BBACBsN54XJ3w3AAAaACOG4WC8"

# Initialize client
ta_client = TextAnalyticsClient(endpoint=TA_ENDPOINT, credential=AzureKeyCredential(TA_KEY))

def detect_language_with_azure(text):
    """
    Detects the language of the input text using Azure Text Analytics.
    Args:
        text (str): The input text from the student
    Returns:
        str: Detected language code ('fr' or 'en')
    """
    response = ta_client.detect_language(documents=[text])[0]
    detected_lang = response.primary_language.iso6391_name.lower()
    return 'fr' if detected_lang == 'fr' else 'en'

# Test cases
if __name__ == "__main__":
    text1 = "Bonjour, comment vas-tu?"
    lang1 = detect_language_with_azure(text1)
    print(f"Text: {text1}, Detected Language: {lang1}")

    text2 = "ALLO"
    lang2 = detect_language_with_azure(text2)
    print(f"Text: {text2}, Detected Language: {lang2}")


    # confident  cost  typescript