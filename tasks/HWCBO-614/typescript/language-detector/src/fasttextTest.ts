import FastText from 'fasttext.js';

async function detectLanguage(text: string): Promise<'fr' | 'en'> {
    try {
        const ft = new FastText({ loadModel: './lid.176.bin' }); // 模型路径
        await ft.load(); // 加载模型
        const result = await ft.predict(text, 1); // 返回 top 1 预测
        const lang = result[0].label.replace('__label__', ''); // 移除前缀
        if (lang === 'fr') return 'fr';
        return 'en'; // 默认英语
    } catch (error) {
        console.error('FastText detection failed:', error);
        return 'en';
    }
}

async function processWithClu(text: string, language: 'fr' | 'en'): Promise<{ result: string }> {
    console.log(`CLU 处理 - 文本: ${text}, 语言: ${language}`);
    return { result: `使用 ${language} 处理完成` };
}

async function runTests() {
    const texts = ["Salut, ça va?", "Hi, how are you?", "Bonjour le monde"];
    for (const text of texts) {
        const lang = await detectLanguage(text);
        const result = await processWithClu(text, lang);
        console.log(result);
    }
}

runTests();