"""
@Time: 2025-03-03
@Auth: Adam Lyu
"""
try:
    from azure.ai.language.conversations import ConversationAnalysisClient
    from azure.core.credentials import AzureKeyCredential
except ImportError as e:
    print("Error: Missing Azure CLU module. Install it with: pip install azure-ai-language-conversations")
    raise e

# CLU configuration
CLU_ENDPOINT = "https://demolyulanguageservice-v2.cognitiveservices.azure.com/"
CLU_KEY = "3pqgnR1fpjcdkAsT2mFRdwk0uLKdId6RGevDc5LDvfYbQDNI2lN7JQQJ99BBACBsN54XJ3w3AAAaACOGCuQH"
CLU_PROJECT_NAME = "Testclu12"
CLU_DEPLOYMENT_NAME = "Testclu12"

# Initialize CLU client
try:
    clu_client = ConversationAnalysisClient(endpoint=CLU_ENDPOINT, credential=AzureKeyCredential(CLU_KEY))
except Exception as e:
    print(f"Error initializing CLU client: {e}")
    raise e

def process_with_clu(text, language):
    """
    Processes the input text with CLU, passing the detected language as a parameter.
    Args:
        text (str): The input text
        language (str): The detected language ('fr' or 'en')
    Returns:
        dict: CLU analysis result
    """
    # CLU request payload, including the language parameter
    clu_payload = {
        "kind": "Conversation",
        "analysisInput": {
            "conversationItem": {
                "id": "PARTICIPANT_ID_HERE",
                "text": text,
                "modality": "text",
                "language": language,
                "participantId": "PARTICIPANT_ID_HERE"
            }
        },
        "parameters": {
            "projectName": CLU_PROJECT_NAME,
            "verbose": True,
            "deploymentName": CLU_DEPLOYMENT_NAME,
            "stringIndexType": "TextElement_V8"
        }
    }

    # Send request to CLU and return result
    try:
        response = clu_client.analyze_conversation(clu_payload)
        prediction = response["result"]["prediction"]
        top_intent = prediction["topIntent"]
        intents = prediction["intents"]

        # Debug: Print the response structure
        print(f"Debug - Full Response: {response}")
        print(f"Debug - Intents: {intents}")

        # Handle intents as a list (if applicable)
        if isinstance(intents, list):
            for intent in intents:
                if intent["category"] == top_intent:
                    return {
                        "intent": top_intent,
                        "confidence": intent["confidenceScore"]
                    }
            return {"intent": top_intent, "confidence": 0.0}  # Fallback if no match
        # Handle intents as a dict (original assumption)
        else:
            return {
                "intent": top_intent,
                "confidence": intents[top_intent]["confidenceScore"]
            }

    except Exception as e:
        print(f"Error processing with CLU: {e}")
        return {"intent": "Unknown", "confidence": 0.0}

# Test the function
if __name__ == "__main__":
    text1 = "Bonjour, comment vas-tu?"
    result1 = process_with_clu(text1, "fr")
    print(f"Text: {text1}, Language: fr, CLU Result: {result1}")

    text2 = "Hello, how are you?"
    result2 = process_with_clu(text2, "en")
    print(f"Text: {text2}, Language: en, CLU Result: {result2}")