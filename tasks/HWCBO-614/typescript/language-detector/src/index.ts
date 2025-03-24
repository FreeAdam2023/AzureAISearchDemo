/**
 * @Time: 2025-03-03
 * @Auth: Adam Lyu
 */

import * as cld from 'cld';

// 定义类型
type LanguageCode = 'fr' | 'en';
type LanguageResult = {
    language: LanguageCode;
    confidence: number;
};

// 测试数据类型
type TestCase = {
    text: string;
    expectedLanguage: LanguageCode;
};

// CLD 语言检测函数
async function detectLanguageWithCld(text: string): Promise<LanguageResult> {
    try {
        const result = await cld.detect(text);
        const topLanguage = result.languages[0]; // 取最可能的语言
        const langCode = topLanguage.code === 'fr' ? 'fr' : 'en'; // 限制为 'fr' 或 'en'
        const confidence = topLanguage.score || topLanguage.percent / 100 || 0; // 获取置信度
        return { language: langCode, confidence };
    } catch (error) {
        console.error('CLD detection failed:', error);
        return { language: 'en', confidence: 0 }; // 错误时返回默认值
    }
}

// 测试数据
const testCases: TestCase[] = [
    { text: "Hello", expectedLanguage: "en" },
    { text: "Hi", expectedLanguage: "en" },
    { text: "Bonjour", expectedLanguage: "fr" },
    { text: "Salut", expectedLanguage: "fr" },
    { text: "Good morning", expectedLanguage: "en" },
    { text: "Bon matin", expectedLanguage: "fr" },
    { text: "How are you", expectedLanguage: "en" },
    { text: "Comment vas-tu", expectedLanguage: "fr" },
    { text: "What’s up", expectedLanguage: "en" },
    { text: "Quoi de neuf", expectedLanguage: "fr" },
    { text: "I’d like to ask a question", expectedLanguage: "en" },
    { text: "J’aimerais poser une question", expectedLanguage: "fr" },
    { text: "I am not feeling well", expectedLanguage: "en" },
    { text: "Je ne me sens pas bien", expectedLanguage: "fr" },
    { text: "What is the Personalized Health Education Program", expectedLanguage: "en" },
    { text: "How can I navigate the Canadian health care system", expectedLanguage: "en" },
    { text: "Où puis-je trouver des ressources de bien-être", expectedLanguage: "fr" },
    { text: "I have a cough that won't go away", expectedLanguage: "en" },
    { text: "J’ai une toux qui ne disparaît pas", expectedLanguage: "fr" },
    { text: "My throat is bothering me", expectedLanguage: "en" },
    { text: "Ma gorge me dérange", expectedLanguage: "fr" },
    { text: "I need a renewal for my prescription", expectedLanguage: "en" },
    { text: "J’ai besoin de renouveler mon ordonnance", expectedLanguage: "fr" },
    { text: "I jammed my finger while playing basketball", expectedLanguage: "en" },
    { text: "Je me suis coincé le doigt en jouant au basket", expectedLanguage: "fr" },
    { text: "My elbow hurts when I bend it", expectedLanguage: "en" },
    { text: "Mon coude me fait mal quand je le plie", expectedLanguage: "fr" },
    { text: "I have shortness of breath when I exercise", expectedLanguage: "en" },
    { text: "J’ai du mal à respirer quand je fais de l’exercice", expectedLanguage: "fr" },
    { text: "Je n’ai plus de questions, merci", expectedLanguage: "fr" },
    { text: "That’s all I needed, bye", expectedLanguage: "en" },
    { text: "C’est tout ce dont j’avais besoin, au revoir", expectedLanguage: "fr" },
    { text: "I think I’m all set, have a great day", expectedLanguage: "en" },
    { text: "Je crois que c’est tout, bonne journée", expectedLanguage: "fr" },
    { text: "I have a sore throat", expectedLanguage: "en" },
    { text: "J’ai mal à la gorge", expectedLanguage: "fr" },
    { text: "I need to get tested for TB", expectedLanguage: "en" },
    { text: "J’ai besoin de me faire tester pour la tuberculose", expectedLanguage: "fr" },
    { text: "I would like to start using some kind of contraception", expectedLanguage: "en" },
    { text: "Je voudrais commencer à utiliser une contraception", expectedLanguage: "fr" },
    { text: "I have pain urinating", expectedLanguage: "en" },
    { text: "J’ai mal en urinant", expectedLanguage: "fr" },
    { text: "I would like to take a pregnancy test", expectedLanguage: "en" },
    { text: "Je voudrais faire un test de grossesse", expectedLanguage: "fr" },
    { text: "I don’t have any more questions, thanks", expectedLanguage: "en" },
    { text: "Merci, je n’ai plus de questions", expectedLanguage: "fr" },
    { text: "I’m good for now. Talk later", expectedLanguage: "en" },
    { text: "Tout est bon pour moi. À bientôt", expectedLanguage: "fr" },
    { text: "I have swelling on my face after an injury", expectedLanguage: "en" },
    { text: "J’ai un gonflement au visage après une blessure", expectedLanguage: "fr" },
];

// 测试函数
async function runTests(): Promise<void> {
    let cldCorrect = 0;
    const total = testCases.length;

    for (const testCase of testCases) {
        // CLD 检测
        const cldResult = await detectLanguageWithCld(testCase.text);
        const cldIsCorrect = cldResult.language === testCase.expectedLanguage;

        // 统计正确数
        if (cldIsCorrect) cldCorrect++;

        // 输出结果
        console.log(`Text: "${testCase.text}"`);
        console.log(`Expected: ${testCase.expectedLanguage}`);
        console.log(`CLD Detected: ${cldResult.language}, Confidence: ${cldResult.confidence}, Result: ${cldIsCorrect ? "Correct" : "Incorrect"}`);
        console.log("---");
    }

    // 计算并输出准确率
    const cldAccuracy = (cldCorrect / total) * 100;
    console.log(`Total Tests: ${total}`);
    console.log(`CLD Correct: ${cldCorrect}, Accuracy: ${cldAccuracy.toFixed(2)}%`);
}

// 执行测试
if (require.main === module) {
    runTests().catch(err => console.error("Test execution failed:", err));
}