import csv

import pandas as pd
import json
import openai
import os
import logging

"""
@Time ： 2024-11-18
@Auth ： Adam Lyu
"""

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("qna_processing.log"),  # 日志文件
        logging.StreamHandler()  # 控制台输出
    ]
)

# 加载 .env 文件中的环境变量
from dotenv import load_dotenv

load_dotenv()

# Azure OpenAI 配置
openai.api_type = os.getenv("OPENAI_API_TYPE")  # 确保是 "azure"
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")  # 例如 "https://<your-resource-name>.openai.azure.com/"
openai.api_version = os.getenv("OPENAI_API_VERSION")  # 例如 "2023-03-15-preview"
engine = os.getenv("OPENAI_DEPLOYMENT_ID")  # 使用部署的模型 ID


class QnAHelper:
    def __init__(self, file_path):
        """
        初始化 QnAHelper 类
        :param file_path: Excel 文件路径
        """
        self.file_path = file_path
        openai.api_type = os.getenv("OPENAI_API_TYPE")  # 确保是 "azure"
        openai.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_base = os.getenv("OPENAI_API_BASE")  # 例如 "https://<your-resource-name>.openai.azure.com/"
        openai.api_version = os.getenv("OPENAI_API_VERSION")  # 例如 "2023-03-15-preview"
        self.engine = os.getenv("OPENAI_DEPLOYMENT_ID")  # 使用部署的模型 ID

    def parse_and_save(self, en_json_path="../result/Question_EN_Response_EN.json",
                       fr_json_path="../result/Question_FR_Response_FR.json"):
        """
        解析 Excel 文件并保存 EN 和 FR 问答对为 JSON 文件
        :param en_json_path: 保存英文问答对的 JSON 文件路径
        :param fr_json_path: 保存法文问答对的 JSON 文件路径
        """
        # 读取 Excel 文件
        try:
            df = pd.read_excel(self.file_path)
        except Exception as e:
            raise ValueError(f"无法读取文件: {self.file_path}. 错误: {e}")

        # 检查必要的列是否存在
        required_columns_en = ["Question EN", "Expected Response EN"]
        required_columns_fr = ["Question FR", "Expected Response FR"]

        missing_columns = [
            col for col in required_columns_en + required_columns_fr if col not in df.columns
        ]
        if missing_columns:
            raise ValueError(f"文件缺少必要列: {missing_columns}")

        # 提取 EN 和 FR 的问答对
        df_en = df[required_columns_en]
        df_fr = df[required_columns_fr]

        # 创建目录（如果不存在）
        os.makedirs(os.path.dirname(en_json_path), exist_ok=True)
        os.makedirs(os.path.dirname(fr_json_path), exist_ok=True)

        # 保存为 JSON 文件
        df_en.to_json(en_json_path, orient="records", force_ascii=False, indent=4)
        df_fr.to_json(fr_json_path, orient="records", force_ascii=False, indent=4)

        logging.info(f"英文问答对已保存为: {en_json_path}")
        logging.info(f"法文问答对已保存为: {fr_json_path}")

    def generate_alternate_questions(self, original_question, n=5):
        """
        调用 Azure OpenAI 生成替代问题。
        :param original_question: 原始问题
        :param n: 替代问题的最大数量
        :return: 替代问题列表
        """
        prompt = f"Generate {n} alternate ways to ask the following question:\nQuestion: {original_question}\nAlternate Questions:"
        try:
            response = openai.ChatCompletion.create(
                engine=self.engine,
                messages=[
                    {"role": "system", "content": "You are an assistant that generates alternate questions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            # 提取生成结果
            alternate_questions = [q.strip() for q in response['choices'][0]['message']['content'].split("\n") if
                                   q.strip()]
            logging.info(f"Generated alternate questions for '{original_question}': {alternate_questions}")
            return alternate_questions
        except Exception as e:
            logging.error(f"Failed to generate alternate questions for '{original_question}': {str(e)}")
            return []

    def generate_synonyms(self, original_question):
        """
        调用 Azure OpenAI 生成同义词。
        :param original_question: 原始问题
        :return: 同义词列表
        """
        prompt = f"Generate synonyms for the following question:\nQuestion: {original_question}\nSynonyms:"
        try:
            response = openai.ChatCompletion.create(
                engine=self.engine,
                messages=[
                    {"role": "system", "content": "You are an assistant that generates synonyms for questions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.7
            )
            # 提取生成结果
            synonyms = [s.strip() for s in response['choices'][0]['message']['content'].split("\n") if s.strip()]
            logging.info(f"Generated synonyms for '{original_question}': {synonyms}")
            return synonyms
        except Exception as e:
            logging.error(f"Failed to generate synonyms for '{original_question}': {str(e)}")
            return []

    def generate_metadata(self, original_question, answer):
        """
        调用 OpenAI API 生成问题的 Metadata。
        :param original_question: 原始问题
        :param answer: 问题对应的答案
        :return: Metadata 字典
        """
        prompt = (
            f"Analyze the following question and answer to generate metadata fields like category, keywords, audience, "
            f"language, and additional information:\n"
            f"Question: {original_question}\n"
            f"Answer: {answer}\n\n"
            f"Metadata fields should include:\n"
            f"- Category (e.g., health_services, general, academic_support)\n"
            f"- Keywords (key terms extracted from the question)\n"
            f"- Audience (e.g., students, staff, visitors)\n"
            f"- Language (e.g., en, fr)\n"
            f"- Additional fields if applicable.\n\n"
            f"Provide the metadata in JSON format."
        )
        try:
            response = openai.ChatCompletion.create(
                engine=self.engine,
                messages=[
                    {"role": "system",
                     "content": "You are an assistant that generates metadata for questions and answers."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            # 解析生成的 Metadata JSON
            metadata = response['choices'][0]['message']['content'].strip()
            metadata_dict = json.loads(metadata)  # 将 JSON 字符串解析为字典
            logging.info(f"Generated metadata for '{original_question}': {metadata_dict}")
            return metadata_dict
        except json.JSONDecodeError as jde:
            logging.error(f"Failed to parse metadata JSON for '{original_question}': {str(jde)}")
            return {}
        except Exception as e:
            logging.error(f"Failed to generate metadata for '{original_question}': {str(e)}")
            return {}

    def process_json_to_tsv(self, input_json_path, output_tsv_path, max_alternates=5):
        """
        Process a JSON file and generate a TSV file that meets the upload file format.
        :param input_json_path: Path to the input JSON file
        :param output_tsv_path: Path to the output TSV file
        :param max_alternates: Maximum number of alternate questions
        """
        try:
            # Read the JSON file
            with open(input_json_path, "r", encoding="utf-8") as infile:
                data = json.load(infile)

            processed_data = []

            for item in data:
                original_question = item.get("Question EN") or item.get("Question FR")
                if not original_question:
                    continue
                answer = item.get("Expected Response EN") or item.get("Expected Response FR")
                if answer:
                    answer = answer.replace("\n", " ").strip()  # Replace newlines with a single space

                # Generate alternate questions
                alternate_questions = self.generate_alternate_questions(original_question, n=max_alternates)

                # Generate synonyms
                synonyms = self.generate_synonyms(original_question)

                # Generate Metadata
                metadata = self.generate_metadata(original_question, answer)
                metadata_str = "|".join([f"{key}:{value}" for key, value in metadata.items()])

                for question in [original_question] + alternate_questions:
                    processed_data.append({
                        "Question": question,
                        "Answer": answer,
                        "Source": "Generated",
                        "Metadata": metadata_str,
                        "SuggestedQuestions": "[]",
                        "IsContextOnly": "False",
                        "Prompts": "[]",
                    })

            # Save as TSV file
            with open(output_tsv_path, "w", encoding="utf-8", newline="") as tsvfile:
                fieldnames = [
                    "Question", "Answer", "Source", "Metadata",
                    "SuggestedQuestions", "IsContextOnly", "Prompts", "QnaId"
                ]
                writer = csv.DictWriter(tsvfile, fieldnames=fieldnames, delimiter="\t")
                writer.writeheader()
                writer.writerows(processed_data)

            logging.info(f"Processed TSV file saved to: {output_tsv_path}")
        except Exception as e:
            logging.error(f"Error while processing JSON file: {str(e)}")

    def generate_test_questions(self, input_json_path, test_json_path, max_alternates=5):
        """
        为每个问题生成测试用替代问题，并单独保存到测试文件中
        :param input_json_path: 输入的 JSON 文件路径
        :param test_json_path: 输出测试文件路径
        :param max_alternates: 为每个问题生成的替代问题数量
        """
        try:
            # 读取 JSON 文件
            with open(input_json_path, "r", encoding="utf-8") as infile:
                data = json.load(infile)

            test_data = []

            for item in data:
                original_question = item.get("Question EN") or item.get("Question FR")
                if not original_question:
                    continue
                answer = item.get("Expected Response EN") or item.get("Expected Response FR")

                # 生成替代问题
                alternate_questions = self.generate_alternate_questions(original_question, n=max_alternates)

                # 保存替代问题和答案
                for alt_question in alternate_questions:
                    test_data.append({"Test Question": alt_question, "Answer": answer})

            # 保存为新的 JSON 文件
            with open(test_json_path, "w", encoding="utf-8") as outfile:
                json.dump(test_data, outfile, ensure_ascii=False, indent=4)

            logging.info(f"Test questions saved to: {test_json_path}")
        except Exception as e:
            logging.error(f"Error while generating test questions: {str(e)}")

    def process_json_to_tsv_without_extra_meta(self):
        import pandas as pd
        import json

        # 定义输入和输出文件路径
        input_file = "../result/Question_EN_Response_EN.json"  # 源 JSON 文件路径
        output_file = "../result/Question_Answer.tsv"  # 目标 TSV 文件路径

        # 读取 JSON 文件
        with open(input_file, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # 处理数据：替换换行符为单个空格并去除空白
        for item in data:
            if "Expected Response EN" in item:
                item["Expected Response EN"] = item["Expected Response EN"].replace("\n", " ").strip()

        # 转换为 DataFrame
        df = pd.DataFrame(data)
        df.columns = ["Question", "Answer"]  # 重命名列

        # 保存为 TSV 文件
        df.to_csv(output_file, sep='\t', index=False, encoding='utf-8')

        print(f"文件已成功保存为 TSV 格式：{output_file}")


# 使用示例
if __name__ == "__main__":
    file_path = "../data/Azure Search vs QnA_31-Oct-2024.xlsx"  # 替换为实际的文件路径
    QnAHelper(file_path).process_json_to_tsv_without_extra_meta()
    # try:
    #     # 初始化 QnAHelper 类，提供 Excel 文件路径
    #     file_path = "../data/Azure Search vs QnA_31-Oct-2024.xlsx"  # 替换为实际的文件路径
    #     qna_helper = QnAHelper(file_path=file_path)
    #
    #     # 步骤 1: 解析 Excel 文件并保存为英文和法文的问答对 JSON 文件
    #     logging.info("开始解析 Excel 文件并生成问答对 JSON 文件...")
    #     qna_helper.parse_and_save(
    #         en_json_path="../result/Question_EN_Response_EN.json",
    #         fr_json_path="../result/Question_FR_Response_FR.json"
    #     )
    #     logging.info("问答对 JSON 文件生成完成！")
    #
    #     # 步骤 2: 处理英文问答对 JSON 文件，生成包含替代问题的 TSV 文件
    #     logging.info("开始处理 JSON 文件并生成 TSV 文件...")
    #     qna_helper.process_json_to_tsv(
    #         input_json_path="../result/Question_EN_Response_EN.json",
    #         output_tsv_path="../result/Question_EN_Response_EN_with_alternates.tsv",
    #         max_alternates=5
    #     )
    #     logging.info("包含替代问题的 TSV 文件生成完成！")
    #
    #     # 步骤 3: 从英文问答对生成测试问题，并保存为 JSON 文件
    #     logging.info("开始生成测试问题 JSON 文件...")
    #     qna_helper.generate_test_questions(
    #         input_json_path="../result/Question_EN_Response_EN.json",
    #         test_json_path="../result/Question_EN_Response_EN_Test_Questions.json",
    #         max_alternates=5
    #     )
    #     logging.info("测试问题 JSON 文件生成完成！")
    #
    #     logging.info("所有任务完成！")
    #
    # except Exception as e:
    #     logging.error(f"程序执行过程中发生错误: {str(e)}")
