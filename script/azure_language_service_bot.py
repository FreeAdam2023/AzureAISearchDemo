"""
@Time: 2024-12-03
@Auth: Adam Lyu
"""

import os
import requests
import json
import pandas as pd
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class AzureLanguageServiceBot:
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
            "filters": {
                "metadataFilter": {
                    "logicalOperation": "OR",
                }
            }
        }
        api_url = f"{self.base_url}/language/:query-knowledgebases"
        params = {
            "projectName": self.project_name,
            "api-version": "2021-10-01",
            "deploymentName": self.deployment_name,
        }

        try:
            # 发送 POST 请求
            response = requests.post(api_url, headers=self.headers, params=params, json=payload)
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
    BOT_SUBSCRIPTION_KEY = os.getenv("BOT_SUBSCRIPTION_KEY")
    BOT_BASE_URL = os.getenv("BOT_BASE_URL")
    BOT_PROJECT_NAME = os.getenv("BOT_PROJECT_NAME")
    INPUT_PATH_TSV = "../result/Question_EN_Response_EN_with_alternates.tsv"
    INPUT_PATH_JSON = "../result/Question_EN_Response_EN_Test_Questions.json"
    OUTPUT_PATH = "../result/Question_EN_Response_Comparison.xlsx"

    bot = AzureLanguageServiceBot(BOT_BASE_URL, BOT_SUBSCRIPTION_KEY, BOT_PROJECT_NAME)

    # 加载问题和期望答案
    questions = load_questions(INPUT_PATH_TSV)
    test_questions = load_questions(INPUT_PATH_JSON)

    # 存储主问题测试结果
    main_results = []

    # 批量提问并对比结果（主问题测试）
    for question_data in questions:
        question = question_data.get("Question", "")
        expected_answer = question_data.get("Answer", "")
        answers = bot.ask_question(question, top=1)

        for answer in answers:
            match = answer["answer"] == expected_answer
            metadata_str = json.dumps(answer.get("metadata", {}))  # 转为字符串以存储
            confidence_score = round(answer.get("confidenceScore", 0), 2)  # 保留 2 位小数
            main_results.append({
                "Question": question,
                "Expected Answer": expected_answer,
                "Bot Answer": answer["answer"],
                "Confidence Score": confidence_score,
                "Metadata": metadata_str,
                "Match": "Yes" if match else "No",
            })

    # 存储测试问题结果
    test_results = []

    # 批量提问并记录结果（测试问题）
    for test_question_data in test_questions:
        test_question = test_question_data.get("Test Question", "")
        expected_answer = test_question_data.get("Answer", "")
        answers = bot.ask_question(test_question, top=1)

        for answer in answers:
            match = answer["answer"] == expected_answer
            metadata_str = json.dumps(answer.get("metadata", {}))  # 转为字符串以存储
            confidence_score = round(answer.get("confidenceScore", 0), 2)  # 保留 2 位小数
            test_results.append({
                "Test Question": test_question,
                "Expected Answer": expected_answer,
                "Bot Answer": answer["answer"],
                "Confidence Score": confidence_score,
                "Metadata": metadata_str,
                "Match": "Yes" if match else "No",
            })

    knowledge_outside_questions = [
        "What is the best restaurant near the campus?",
        "How do I rent a bike in Ottawa?",
        "What is the weather today?",
        "Where can I find the nearest library?",
        "Are there any hiking trails close to the campus?",
        "How do I apply for a parking permit in Ottawa?",
        "What are the opening hours of the nearest grocery store?",
        "How do I join a local sports team?",
        "Where can I buy public transport tickets in Ottawa?",
        "What is the best way to get to downtown Ottawa from campus?"
    ]

    # 存储测试问题结果
    outside_results = []

    for test_question_data in knowledge_outside_questions:
        test_question = test_question_data
        answers = bot.ask_question(test_question, top=1)

        for answer in answers:
            metadata_str = json.dumps(answer.get("metadata", {}))  # 转为字符串以存储
            confidence_score = round(answer.get("confidenceScore", 0), 2)  # 保留 2 位小数
            outside_results.append({
                "Test Question": test_question,
                "Bot Answer": answer["answer"],
                "Confidence Score": confidence_score,
            })

    # 将主问题结果和测试问题结果保存到 Excel 文件
    with pd.ExcelWriter(OUTPUT_PATH, engine="xlsxwriter") as writer:
        pd.DataFrame(main_results).to_excel(writer, index=False, sheet_name="Main Questions")
        pd.DataFrame(test_results).to_excel(writer, index=False, sheet_name="Test Questions")
        pd.DataFrame(outside_results).to_excel(writer, index=False, sheet_name="Outside Questions")

    print(f"Results saved to {OUTPUT_PATH}")
