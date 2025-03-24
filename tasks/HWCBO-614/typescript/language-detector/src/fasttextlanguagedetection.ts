const LanguageDetection = require("@smodin/fast-text-language-detection");

const lid = new LanguageDetection();

const testCases = [
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

async function testLanguageDetection() {
    let correctCount = 0;
    const failedCases = [];

    for (const { text, expectedLanguage } of testCases) {
        const detectedLanguages = await lid.predict(text);
        const detectedLanguage = detectedLanguages[0]?.lang || "unknown";
        const isCorrect = detectedLanguage === expectedLanguage;
        if (isCorrect) {
            correctCount++;
        } else {
            failedCases.push({ text, expectedLanguage, detectedLanguage });
        }

        console.log(`Text: "${text}" | Expected: ${expectedLanguage} | Detected: ${detectedLanguage} | ${isCorrect ? "✅" : "❌"}`);
    }

    const accuracy = (correctCount / testCases.length * 100).toFixed(2);
    console.log(`\n✅ Total Correct: ${correctCount}/${testCases.length}`);
    console.log(`📊 Accuracy: ${accuracy}%`);

    if (failedCases.length > 0) {
        console.log("\n❗ Failed Cases:");
        failedCases.forEach(({ text, expectedLanguage, detectedLanguage }) => {
            console.log(`- Text: "${text}"`);
            console.log(`  Expected: ${expectedLanguage} | Detected: ${detectedLanguage}`);
        });
    } else {
        console.log("\n🎉 All test cases passed!");
    }
}

testLanguageDetection();
