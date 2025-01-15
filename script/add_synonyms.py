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


def load_json(file_path):
    """
    加载 JSON 文件
    :param file_path: 文件路径
    :return: JSON 数据
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        logging.info(f"Loaded JSON file: {file_path}")
        return data
    except Exception as e:
        logging.error(f"Failed to load JSON file {file_path}: {str(e)}")
        raise


def save_json(data, file_path):
    """
    保存 JSON 数据到文件
    :param data: 要保存的 JSON 数据
    :param file_path: 保存路径
    """
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        logging.info(f"Saved updated JSON to: {file_path}")
    except Exception as e:
        logging.error(f"Failed to save JSON file {file_path}: {str(e)}")
        raise


def generate_synonyms(list_key):
    """
    调用 Azure OpenAI API 生成同义词，并清洗结果
    :param list_key: 输入的关键词
    :return: 同义词列表
    """
    prompt = f"List synonyms for the term '{list_key}' as a comma-separated list."
    try:
        response = openai.ChatCompletion.create(
            engine="gpt-4o",  # 替换为你部署的模型名称
            messages=[
                {"role": "system",
                 "content": "You are a helpful assistant that provides a clean, comma-separated list of synonyms for given terms."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50,
            temperature=0.5,
            top_p=0.9,
            frequency_penalty=0,
            presence_penalty=0,
        )
        synonyms_content = response['choices'][0]['message']['content']

        # 提取纯单词或短语，去除多余描述
        synonyms = re.findall(r'\b[a-zA-Z\s-]+\b', synonyms_content)
        synonyms = [syn.strip() for syn in synonyms if syn.strip()]

        return list(set(synonyms))  # 去重
    except openai.error.OpenAIError as e:
        logging.error(f"Error while generating synonyms for '{list_key}': {e}")
        return []


def update_synonyms(data):
    """
    更新 JSON 数据中的同义词
    :param data: 原始 JSON 数据
    :return: 更新后的 JSON 数据
    """
    entities = data.get("assets", {}).get("entities", [])
    for entity in entities:
        sublists = entity.get("list", {}).get("sublists", [])
        for sublist in sublists:
            list_key = sublist.get("listKey", "")
            if list_key:
                time.sleep(10)
                synonyms = generate_synonyms(list_key)
                for synonym_entry in sublist.get("synonyms", []):
                    if synonym_entry.get("language") == "en-us":
                        existing_values = synonym_entry.get("values", [])
                        synonym_entry["values"] = list(set(existing_values + synonyms))
                        logging.info(f"Updated synonyms for listKey '{list_key}': {synonym_entry['values']}")
    return data

def main():
    """
    主程序入口
    """
    input_file = "../typescriptdemo/NewCLU_Testing.json"
    output_file = "Updated_NewCLU_Testing.json"

    try:
        # 验证配置

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
