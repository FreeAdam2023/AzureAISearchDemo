import os
import requests
import json
import pandas as pd
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class AzureLanguageServiceBotSimple:
    def __init__(self, base_url, subscription_key, project_name, deployment_name="production"):
        """
        初始化 Azure Language Service Bot 类
        :param base_url: Azure 服务的基础 URL
        :param subscription_key: Azure 服务的订阅密钥
        :param project_name: 项目名称（知识库名）
        :param deployment_name: 部署名称，默认为 production
        """
        self.base_url = base_url.rstrip("/")
        self.subscription_key = subscription_key
        self.project_name = project_name
        self.deployment_name = deployment_name
        self.api_url = f"{self.base_url}/language/:query-knowledgebases"
        self.headers = {
            "Content-Type": "application/json",
            "Ocp-Apim-Subscription-Key": self.subscription_key,
        }

    def ask_question(self, question, top=3, confidence_threshold=0.3):
        """
        向 QnA 服务提问并获取答案
        :param question: 用户的问题
        :param top: 返回的答案数量，默认 3
        :param confidence_threshold: 答案的信心分数阈值，默认 0.3
        :return: 答案列表
        """
        payload = {
            "top": top,
            "question": question,
            "includeUnstructuredSources": True,
            "confidenceScoreThreshold": confidence_threshold,
            "answerSpanRequest": {
                "enable": True,
                "topAnswersWithSpan": 1,
                "confidenceScoreThreshold": confidence_threshold,
            },
        }
        params = {
            "projectName": self.project_name,
            "api-version": "2021-10-01",
            "deploymentName": self.deployment_name,
        }

        try:
            # 发送 POST 请求
            response = requests.post(self.api_url, headers=self.headers, params=params, json=payload)
            response.raise_for_status()
            response_data = response.json()
            return response_data.get("answers", [])
        except requests.exceptions.RequestException as e:
            return [{"answer": f"HTTP Error: {str(e)}", "confidenceScore": 0, "metadata": {}}]
        except Exception as e:
            return [{"answer": f"Unexpected error: {str(e)}", "confidenceScore": 0, "metadata": {}}]


def load_questions(input_path):
    """
    从文件中加载问题和期望答案
    :param input_path: 文件路径
    :return: 问题列表
    """
    if input_path.endswith(".tsv"):
        return pd.read_csv(input_path, sep="\t").to_dict(orient="records")
    elif input_path.endswith(".json"):
        with open(input_path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        raise ValueError("Unsupported file format. Please provide a .tsv or .json file.")


def save_to_excel(results, output_path):
    """
    将对比结果保存到 Excel 文件
    :param results: 对比结果
    :param output_path: 输出路径
    """
    df = pd.DataFrame(results)
    df.to_excel(output_path, index=False)
    print(f"Results saved to {output_path}")


if __name__ == "__main__":
    SIMPLE_BOT_SUBSCRIPTION_KEY = os.getenv("SIMPLE_BOT_SUBSCRIPTION_KEY")
    SIMPLE_BOT_BASE_URL = os.getenv("SIMPLE_BOT_BASE_URL")
    SIMPLE_BOT_PROJECT_NAME = os.getenv("SIMPLE_BOT_PROJECT_NAME")
    INPUT_PATH_MAIN = "../result/Question_Answer.tsv"
    INPUT_PATH_TEST = "../result/Question_EN_Response_EN_Test_Questions.json"
    OUTPUT_PATH_MAIN = "../result/Question_Answer_Comparison_Main.xlsx"
    OUTPUT_PATH_TEST = "../result/Question_Answer_Comparison_Test.xlsx"

    # 初始化机器人
    bot = AzureLanguageServiceBotSimple(SIMPLE_BOT_BASE_URL, SIMPLE_BOT_SUBSCRIPTION_KEY, SIMPLE_BOT_PROJECT_NAME)

    # 处理主问题
    questions = load_questions(INPUT_PATH_MAIN)
    results_main = []

    for question_data in questions:
        question = question_data.get("Question", "")
        expected_answer = question_data.get("Answer", "")
        answers = bot.ask_question(question, top=1)

        for answer in answers:
            bot_answer = answer.get("answer", "")
            confidence_score = round(answer.get("confidenceScore", 0), 2)  # 保留 2 位小数
            match = "Yes" if bot_answer.strip() == expected_answer.strip() else "No"
            results_main.append({
                "Question": question,
                "Expected Answer": expected_answer,
                "Bot Answer": bot_answer,
                "Confidence Score": confidence_score,
                "Match": match,
            })

    save_to_excel(results_main, OUTPUT_PATH_MAIN)

    # 处理测试问题
    test_questions = load_questions(INPUT_PATH_TEST)
    results_test = []

    for test_question_data in test_questions:
        test_question = test_question_data.get("Test Question", "")
        expected_answer = test_question_data.get("Answer", "")
        answers = bot.ask_question(test_question, top=1)

        for answer in answers:
            bot_answer = answer.get("answer", "")
            confidence_score = round(answer.get("confidenceScore", 2))  # 保留 2 位小数
            match = "Yes" if bot_answer.strip() == expected_answer.strip() else "No"
            results_test.append({
                "Test Question": test_question,
                "Expected Answer": expected_answer,
                "Bot Answer": bot_answer,
                "Confidence Score": confidence_score,
                "Match": match,
            })

    save_to_excel(results_test, OUTPUT_PATH_TEST)
