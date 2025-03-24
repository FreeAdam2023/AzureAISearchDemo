"""
@Time: 2025-03-03
@Auth: Adam Lyu
"""

import fasttext

# Load pretrained model (ensure lid.176.bin is in the same directory)
model = fasttext.load_model('lid.176.bin')

# 定义类型（Python 中没有显式类型，但为了清晰起见，记录预期类型）
def detect_language_fasttext(text: str) -> str:
    """
    Detects the language of the input text using fasttext, returning 'fr' or 'en'.
    Args:
        text (str): The text input by the student
    Returns:
        str: The detected language ('fr' or 'en')
    """
    prediction = model.predict(text)
    detected_lang = prediction[0][0].replace('__label__', '')  # Extract language code
    if detected_lang == 'fr':
        return 'fr'
    elif detected_lang == 'en':
        return 'en'
    else:
        return 'en'  # Default to English

# 测试数据
test_cases = [
    {"text": "Hello", "expected_language": "en"},
    {"text": "Hi", "expected_language": "en"},
    {"text": "Bonjour", "expected_language": "fr"},
    {"text": "Salut", "expected_language": "fr"},
    {"text": "Good morning", "expected_language": "en"},
    {"text": "Bon matin", "expected_language": "fr"},
    {"text": "How are you", "expected_language": "en"},
    {"text": "Comment vas-tu", "expected_language": "fr"},
    {"text": "What’s up", "expected_language": "en"},
    {"text": "Quoi de neuf", "expected_language": "fr"},
    {"text": "I’d like to ask a question", "expected_language": "en"},
    {"text": "J’aimerais poser une question", "expected_language": "fr"},
    {"text": "I am not feeling well", "expected_language": "en"},
    {"text": "Je ne me sens pas bien", "expected_language": "fr"},
    {"text": "What is the Personalized Health Education Program", "expected_language": "en"},
    {"text": "How can I navigate the Canadian health care system", "expected_language": "en"},
    {"text": "Où puis-je trouver des ressources de bien-être", "expected_language": "fr"},
    {"text": "I have a cough that won't go away", "expected_language": "en"},
    {"text": "J’ai une toux qui ne disparaît pas", "expected_language": "fr"},
    {"text": "My throat is bothering me", "expected_language": "en"},
    {"text": "Ma gorge me dérange", "expected_language": "fr"},
    {"text": "I need a renewal for my prescription", "expected_language": "en"},
    {"text": "J’ai besoin de renouveler mon ordonnance", "expected_language": "fr"},
    {"text": "I jammed my finger while playing basketball", "expected_language": "en"},
    {"text": "Je me suis coincé le doigt en jouant au basket", "expected_language": "fr"},
    {"text": "My elbow hurts when I bend it", "expected_language": "en"},
    {"text": "Mon coude me fait mal quand je le plie", "expected_language": "fr"},
    {"text": "I have shortness of breath when I exercise", "expected_language": "en"},
    {"text": "J’ai du mal à respirer quand je fais de l’exercice", "expected_language": "fr"},
    {"text": "Je n’ai plus de questions, merci", "expected_language": "fr"},
    {"text": "That’s all I needed, bye", "expected_language": "en"},
    {"text": "C’est tout ce dont j’avais besoin, au revoir", "expected_language": "fr"},
    {"text": "I think I’m all set, have a great day", "expected_language": "en"},
    {"text": "Je crois que c’est tout, bonne journée", "expected_language": "fr"},
    {"text": "I have a sore throat", "expected_language": "en"},
    {"text": "J’ai mal à la gorge", "expected_language": "fr"},
    {"text": "I need to get tested for TB", "expected_language": "en"},
    {"text": "J’ai besoin de me faire tester pour la tuberculose", "expected_language": "fr"},
    {"text": "I would like to start using some kind of contraception", "expected_language": "en"},
    {"text": "Je voudrais commencer à utiliser une contraception", "expected_language": "fr"},
    {"text": "I have pain urinating", "expected_language": "en"},
    {"text": "J’ai mal en urinant", "expected_language": "fr"},
    {"text": "I would like to take a pregnancy test", "expected_language": "en"},
    {"text": "Je voudrais faire un test de grossesse", "expected_language": "fr"},
    {"text": "I don’t have any more questions, thanks", "expected_language": "en"},
    {"text": "Merci, je n’ai plus de questions", "expected_language": "fr"},
    {"text": "I’m good for now. Talk later", "expected_language": "en"},
    {"text": "Tout est bon pour moi. À bientôt", "expected_language": "fr"},
    {"text": "I have swelling on my face after an injury", "expected_language": "en"},
    {"text": "J’ai un gonflement au visage après une blessure", "expected_language": "fr"},
]

# 测试函数
def run_tests():
    correct = 0
    total = len(test_cases)

    for test_case in test_cases:
        text = test_case["text"]
        expected_language = test_case["expected_language"]

        # FastText 检测
        detected_language = detect_language_fasttext(text)
        is_correct = detected_language == expected_language

        # 统计正确数
        if is_correct:
            correct += 1

        # 输出结果
        print(f"Text: \"{text}\"")
        print(f"Expected: {expected_language}")
        print(f"FastText Detected: {detected_language}, Result: {'Correct' if is_correct else 'Incorrect'}")
        print("---")

    # 计算并输出准确率
    accuracy = (correct / total) * 100
    print(f"Total Tests: {total}")
    print(f"Correct: {correct}")
    print(f"Accuracy: {accuracy:.2f}%")

# 执行测试
if __name__ == "__main__":
    run_tests()