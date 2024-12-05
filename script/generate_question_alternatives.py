import openai
import pandas as pd
from dotenv import load_dotenv
import os
import logging

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("context_generation.log"),
        logging.StreamHandler()
    ]
)

# 加载环境变量
load_dotenv()

# Azure OpenAI 配置
openai.api_type = os.getenv("OPENAI_API_TYPE")
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = os.getenv("OPENAI_API_VERSION")
engine = os.getenv("OPENAI_DEPLOYMENT_ID")

# 文件路径
input_file = "../result/testqnasCaseManagement_en_azure.tsv"
output_file = "../result/testqnasCaseManagement_en_azure_with_context.xlsx"

# 生成替代问题
def generate_alternative_questions(question):
    prompt = f"""
    Generate up to 4 alternative phrasing versions for the following question. Ensure they maintain the original intent and are easy to understand:
    Question: "{question}"
    Alternatives:
    """
    try:
        response = openai.ChatCompletion.create(
            engine=engine,
            messages=[
                {"role": "system",
                 "content": "You are an assistant that generates alternative versions of questions for Q&A systems."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )
        alternatives = response['choices'][0]['message']['content'].strip().split("\n")
        logging.info(f"Generated alternatives for question: '{question}' -> {alternatives}")
        return [alt.strip("- ").strip() for alt in alternatives[:4]]  # 返回最多 4 个版本
    except Exception as e:
        logging.error(f"Failed to generate alternatives for question: '{question}' - Error: {str(e)}")
        return ["No alternatives generated due to error."] * 4  # 确保返回 4 个空值

# 生成上下文描述
def generate_context_description(question, answer, metadata):
    prompt = f"""
    Based on the following question, answer, and metadata, generate a concise and clear context description:
    Question: {question}
    Answer: {answer}
    Metadata: {metadata}
    Context Description:
    """
    try:
        response = openai.ChatCompletion.create(
            engine=engine,
            messages=[
                {"role": "system",
                 "content": "You are an assistant that generates context descriptions for Q&A pairs."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        context = response['choices'][0]['message']['content'].strip()
        logging.info(f"Generated context for question: '{question}' -> {context}")
        return context
    except Exception as e:
        logging.error(f"Failed to generate context for question: '{question}' - Error: {str(e)}")
        return "No context generated due to error."

# 处理 TSV 文件并导出为 Excel
def process_questions_with_context(input_file, output_file):
    try:
        # 读取 TSV 文件
        df = pd.read_csv(input_file, sep="\t")

        # 初始化结果数据
        results = []

        for _, row in df.iterrows():
            question = row["Question"]
            answer = row["Answer"]
            metadata = row["Metadata"]

            # 生成替代问题
            alternatives = generate_alternative_questions(question)
            alt_1, alt_2, alt_3, alt_4 = alternatives  # 确保替代问题分配到 4 列

            # 生成上下文描述
            context = generate_context_description(question, answer, metadata)

            # 记录结果
            results.append({
                "Original Question": question,
                "Answer": answer,
                "Metadata": metadata,
                "Context": context,
                "Alternative Question 1": alt_1,
                "Alternative Question 2": alt_2,
                "Alternative Question 3": alt_3,
                "Alternative Question 4": alt_4
            })

        # 转换为 DataFrame 并保存为 Excel
        result_df = pd.DataFrame(results)
        result_df.to_excel(output_file, index=False, sheet_name="Alternatives with Context")
        logging.info(f"Processed file with alternatives and context saved to: {output_file}")
    except Exception as e:
        logging.error(f"Error while processing questions with context: {str(e)}")

# 执行主函数
if __name__ == "__main__":
    process_questions_with_context(input_file, output_file)
