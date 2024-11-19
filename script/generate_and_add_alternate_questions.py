"""
@Time ： 2024-11-18
@Auth ： Adam Lyu
"""
import openai
import csv
from dotenv import load_dotenv
import os
import logging

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
load_dotenv()

# Azure OpenAI 配置
openai.api_type = os.getenv("OPENAI_API_TYPE")  # 确保是 "azure"
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")  # 例如 "https://<your-resource-name>.openai.azure.com/"
openai.api_version = os.getenv("OPENAI_API_VERSION")  # 例如 "2023-03-15-preview"
engine = os.getenv("OPENAI_DEPLOYMENT_ID")  # 使用部署的模型 ID

# 文件路径
input_file = "../result/testqnasCaseManagement_en_azure.tsv"  # 输入的 TSV 文件
output_file = "../result/testqnasCaseManagement_en_azure_with_alternates.tsv"  # 输出的 TSV 文件


# 生成替代问题
def generate_alternate_questions(original_question, n=5):
    prompt = f"Generate {n} alternate ways to ask the following question:\nQuestion: {original_question}\nAlternate Questions:"
    try:
        response = openai.ChatCompletion.create(
            engine=engine,  # 替换为 Azure 部署的模型 ID
            messages=[
                {"role": "system", "content": "You are an assistant that generates alternate questions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )
        # 提取生成结果
        alternate_questions = [q.strip() for q in response['choices'][0]['message']['content'].strip().split("\n")]
        logging.info(f"Generated alternate questions for: '{original_question}' -> {alternate_questions}")
        return alternate_questions
    except Exception as e:
        logging.error(f"Failed to generate alternate questions for: '{original_question}' - Error: {str(e)}")
        return []


# 处理 TSV 文件
def process_tsv_file(input_file, output_file, max_alternates=5):
    try:
        with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8",
                                                                     newline="") as outfile:
            reader = csv.DictReader(infile, delimiter="\t")
            fieldnames = ["Question", "Answer", "Metadata"]
            writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter="\t")

            # 写入表头
            writer.writeheader()

            for row in reader:
                original_question = row["Question"]
                answer = row["Answer"]
                metadata = row["Metadata"]

                # 生成替代问题
                alternate_questions = generate_alternate_questions(original_question, n=max_alternates)

                # 写入原问题
                writer.writerow({"Question": original_question, "Answer": answer, "Metadata": metadata})

                # 写入替代问题
                for alt_question in alternate_questions:
                    writer.writerow({"Question": alt_question, "Answer": answer, "Metadata": metadata})

        logging.info(f"Processed file saved to: {output_file}")
    except Exception as e:
        logging.error(f"Error while processing TSV file: {str(e)}")


# 执行主函数
if __name__ == "__main__":
    process_tsv_file(input_file, output_file, max_alternates=5)
    # import openai
    # from dotenv import load_dotenv
    # import os
    #
    # # 加载 .env 文件
    # load_dotenv()
    #
    # # Azure OpenAI 配置
    # openai.api_type = os.getenv("OPENAI_API_TYPE")  # 必须是 "azure"
    # openai.api_key = os.getenv("OPENAI_API_KEY")
    # openai.api_base = os.getenv("OPENAI_API_BASE")
    # openai.api_version = os.getenv("OPENAI_API_VERSION")
    # engine = os.getenv("OPENAI_DEPLOYMENT_ID")  # 部署名称
    #
    # # 测试调用
    # try:
    #     response = openai.ChatCompletion.create(
    #         engine=engine,
    #         messages=[
    #             {"role": "system", "content": "You are a helpful assistant."},
    #             {"role": "user", "content": "What is Azure OpenAI?"}
    #         ],
    #         max_tokens=50,
    #         temperature=0.7
    #     )
    #     print(response['choices'][0]['message']['content'])
    # except Exception as e:
    #     print(f"Error: {e}")
    #
