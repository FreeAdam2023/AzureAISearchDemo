import os
import json
import re
import logging
import time

import openai
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# Azure OpenAI 配置
openai.api_type = "azure"
openai.api_base = os.getenv("OPENAI_API_BASE", "https://adam-m4ww5pgc-eastus2.openai.azure.com/")
openai.api_version = os.getenv("OPENAI_API_VERSION")
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("synonyms_update.log"),
        logging.StreamHandler()
    ]
)

# 缓存生成的同义词
synonyms_cache = {}


def load_json(file_path):
    """加载 JSON 文件"""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        logging.info(f"Loaded JSON file: {file_path}")
        return data
    except Exception as e:
        logging.error(f"Failed to load JSON file {file_path}: {str(e)}")
        raise


def save_json(data, file_path):
    """保存 JSON 数据到文件"""
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        logging.info(f"Saved updated JSON to: {file_path}")
    except Exception as e:
        logging.error(f"Failed to save JSON file {file_path}: {str(e)}")
        raise


def generate_synonyms_and_typos(list_key, retries=3):
    """调用 Azure OpenAI API 生成同义词和常见拼写错误"""
    global synonyms_cache
    if list_key in synonyms_cache:
        return synonyms_cache[list_key]

    prompt = f"""
    List synonyms and common misspellings for the term '{list_key}' as a comma-separated list. Include variations where:
    - Letters are swapped (e.g., 'teh' for 'the').
    - A letter is missing (e.g., 'helo' for 'hello').
    - An extra letter is added (e.g., 'helllo' for 'hello').
    - Similar-sounding substitutions (e.g., 'there' for 'their').
    """
    for attempt in range(retries):
        try:
            response = openai.ChatCompletion.create(
                engine="gpt-4o",  # 替换为你部署的模型名称
                messages=[
                    {"role": "system",
                     "content": "You are a helpful assistant that provides valid synonyms and common misspellings for given terms."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.5,
                top_p=0.9,
                frequency_penalty=0,
                presence_penalty=0,
            )
            synonyms_content = response['choices'][0]['message']['content']
            # 提取有效的单词或短语
            synonyms = re.findall(r'\b[a-zA-Z\s-]+\b', synonyms_content)
            synonyms = [syn.strip() for syn in synonyms if syn.strip()]
            synonyms_cache[list_key] = list(set(synonyms))  # 缓存结果并去重
            return synonyms_cache[list_key]
        except openai.error.OpenAIError as e:
            logging.warning(f"Attempt {attempt + 1} failed for listKey '{list_key}': {e}")
            time.sleep(2)  # 等待 2 秒后重试
    logging.error(f"Failed to generate synonyms and typos for '{list_key}' after {retries} retries.")
    return []

def update_synonyms(data):
    """更新 JSON 数据中的同义词和拼写错误"""
    entities = data.get("assets", {}).get("entities", [])
    for entity in entities:
        sublists = entity.get("list", {}).get("sublists", [])
        for sublist in sublists:
            time.sleep(10)
            list_key = sublist.get("listKey", "")
            if list_key:
                logging.info(f"Processing listKey: {list_key}")
                synonyms_and_typos = generate_synonyms_and_typos(list_key)
                if synonyms_and_typos:
                    for synonym_entry in sublist.get("synonyms", []):
                        if synonym_entry.get("language") == "en-us":
                            existing_values = synonym_entry.get("values", [])
                            updated_values = list(set(existing_values + synonyms_and_typos))
                            synonym_entry["values"] = updated_values
                            logging.info(f"Updated synonyms and typos for listKey '{list_key}': {updated_values}")
    return data



def main():
    """主程序入口"""
    input_file = "../typescriptdemo/NewCLU_Testing.json"
    output_file = "Updated_NewCLU_Testing.json"

    try:
        # 加载 JSON 数据
        data = load_json(input_file)

        # 更新同义词
        updated_data = update_synonyms(data)

        # 保存更新后的 JSON 数据
        save_json(updated_data, output_file)

        logging.info("Synonyms have been added and the file has been updated successfully.")
    except Exception as e:
        logging.error(f"An error occurred during processing: {str(e)}")


if __name__ == "__main__":
    main()
