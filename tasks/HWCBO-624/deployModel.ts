import axios from "axios";
import * as dotenv from "dotenv";

dotenv.config();

// 读取环境变量
const API_KEY = process.env.AZURE_API_KEY!;
const ENDPOINT = process.env.AZURE_ENDPOINT!;
const PROJECT_NAME = process.env.PROJECT_NAME!;
const DEPLOYMENT_NAME = process.env.DEPLOYMENT_NAME!;
const F1_SCORE_THRESHOLD = parseFloat(process.env.F1_SCORE_THRESHOLD!);
const PRECISION_THRESHOLD = parseFloat(process.env.PRECISION_THRESHOLD!);
const RECALL_THRESHOLD = parseFloat(process.env.RECALL_THRESHOLD!);
// const WEBHOOK_URL = process.env.WEBHOOK_URL!;

// Azure CLU 评估 API
const MODEL_EVAL_URL = `${ENDPOINT}/language/query-knowledgebases/v1.0/projects/${PROJECT_NAME}/evaluations/${DEPLOYMENT_NAME}`;

async function getModelPerformance() {
    try {
        const response = await axios.get(MODEL_EVAL_URL, {
            headers: {
                "Ocp-Apim-Subscription-Key": API_KEY,
                "Content-Type": "application/json",
            },
        });

        const data = response.data;
        const performance = {
            intentF1: data.intentF1Score,
            entityF1: data.entityF1Score,
            precision: data.precisionScore,
            recall: data.recallScore,
            confusionMatrix: data.confusionMatrix,
            falseNegative: data.falseNegativeCount,
            falsePositive: data.falsePositiveCount
        };

        console.log("🔍 模型评估数据:", performance);
        return performance;
    } catch (error) {
        console.error("❌ 获取模型性能数据失败:", error);
        // process.exit(1); // 终止 CI/CD 进程
    }
}

// 发送通知（Webhook / Slack / Email）
async function sendNotification(message: string) {
    try {
        // await axios.post(WEBHOOK_URL, { text: message });
        console.log("📢 已发送通知:", message);
    } catch (error) {
        console.error("❌ 发送通知失败:", error);
    }
}

// 评估并决定是否部署
async function evaluateAndDeploy() {
    console.log("🚀 开始检查模型性能...");

    const performance = await getModelPerformance();

    // 设定判断标准
    const isIntentGood = performance.intentF1 >= F1_SCORE_THRESHOLD;
    const isPrecisionGood = performance.precision >= PRECISION_THRESHOLD;
    const isRecallGood = performance.recall >= RECALL_THRESHOLD;
    const isFalseNegativesLow = performance.falseNegative < 10; // 可调整
    const isFalsePositivesLow = performance.falsePositive < 10; // 可调整

    if (isIntentGood && isPrecisionGood && isRecallGood && isFalseNegativesLow && isFalsePositivesLow) {
        console.log(`✅ 模型通过评估 (Intent F1: ${performance.intentF1}), 开始部署到生产...`);
        await sendNotification(`✅ 模型通过评估 (Intent F1: ${performance.intentF1}), 正在部署...`);
        // 这里可以调用部署 API
    } else {
        console.log(`❌ 模型未通过评估 (Intent F1: ${performance.intentF1})，停止部署`);
        await sendNotification(`❌ 模型评估未通过，部署已停止。\n性能数据: ${JSON.stringify(performance, null, 2)}`);
        // process.exit(1); // 终止 CI/CD 进程
    }
}

// 运行主流程
evaluateAndDeploy();
