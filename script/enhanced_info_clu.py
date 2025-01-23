import os
import json
import logging
import time

import openai
from dotenv import load_dotenv

# load evn
load_dotenv()

# Azure OpenAI config
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

# cache
synonyms_cache = {}


def load_json(file_path):
    """load JSON file"""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        logging.info(f"Loaded JSON file: {file_path}")
        return data
    except Exception as e:
        logging.error(f"Failed to load JSON file {file_path}: {str(e)}")
        raise


def save_json(data, file_path):
    """save JSON data to file"""
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        logging.info(f"Saved updated JSON to: {file_path}")
    except Exception as e:
        logging.error(f"Failed to save JSON file {file_path}: {str(e)}")
        raise


def generate_synonyms_and_typos(list_key, retries=3):
    """call Azure OpenAI API generate synonyms and typos, and return word list only """
    global synonyms_cache
    if list_key in synonyms_cache:
        return synonyms_cache[list_key]

    prompt = f"""
    Provide a comma-separated list of synonyms and common misspellings for the term '{list_key}'. Only include the terms themselves without any additional headings or descriptions.
    """
    for attempt in range(retries):
        try:
            time.sleep(10)
            response = openai.ChatCompletion.create(
                engine="gpt-4o",
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
            # extract specific word and phrase
            synonyms = [term.strip() for term in synonyms_content.split(",") if term.strip()]
            synonyms_cache[list_key] = list(set(synonyms))  # cache result and Remove duplicates
            return synonyms_cache[list_key]
        except openai.error.OpenAIError as e:
            logging.warning(f"Attempt {attempt + 1} failed for listKey '{list_key}': {e}")
            time.sleep(2)  # wait 2 seconds then retry
    logging.error(f"Failed to generate synonyms and typos for '{list_key}' after {retries} retries.")
    return []


def update_synonyms(data):
    """update JSON data synonyms and typos"""
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
    input_file = "../typescriptdemo/NewCLU_Testing.json"
    output_file = "Updated_NewCLU_Testing.json"

    try:
        data = load_json(input_file)
        updated_data = update_synonyms(data)
        save_json(updated_data, output_file)
        logging.info("Synonyms have been added and the file has been updated successfully.")
    except Exception as e:
        logging.error(f"An error occurred during processing: {str(e)}")


if __name__ == "__main__":
    main()
