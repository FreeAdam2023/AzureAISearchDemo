import * as cld from 'cld';

async function detectLanguage(text: string): Promise<{ language: 'fr' | 'en', confidence: number }> {
    try {
        const result = await cld.detect(text);
        const topLanguage = result.languages[0]; // 取最可能的语言
        const langCode = topLanguage.code === 'fr' ? 'fr' : 'en'; // 限制为 'fr' 或 'en'
        const confidence = topLanguage.score || topLanguage.percent / 100 || 0; // 获取置信度（视库而定）

        console.log(`检测结果: ${text} -> 语言: ${langCode}, 置信度: ${confidence}`);
        return { language: langCode, confidence };
    } catch (error) {
        console.error('CLD detection failed:', error);
        return { language: 'en', confidence: 0 }; // 错误时返回默认值
    }
}

async function processWithClu(text: string, language: 'fr' | 'en', confidence: number): Promise<{ result: string }> {
    if (confidence < 0.7) { // 设置置信度阈值
        console.warn(`警告: 置信度 ${confidence} 过低，可能检测不准确`);
    }
    console.log(`CLU 处理 - 文本: ${text}, 语言: ${language}, 置信度: ${confidence}`);
    return { result: `使用 ${language} 处理完成` };
}

async function runTests() {
    const texts = ["Salut, ça va?", "Hi, how are you?", "Bonjour hi"]; // 添加混杂语言测试
    for (const text of texts) {
        const { language, confidence } = await detectLanguage(text);
        const result = await processWithClu(text, language, confidence);
        console.log(result);
    }
}

runTests();