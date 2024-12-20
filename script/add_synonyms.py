"""
@Time ： 2024-12-19
@Auth ： Adam Lyu
"""
import os
import json
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()
# OpenAI API configuration


OPENAI_API_URL = os.getenv("OPENAI_API_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}"
}

# Load the JSON file
with open("NewCLU_Testing.json", "r", encoding="utf-8") as file:
    data = json.load(file)


# Helper function to generate synonyms
def generate_synonyms(list_key):
    prompt = f"Provide synonyms for the term: '{list_key}'"
    payload = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that provides synonyms for given terms."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 50
    }
    response = requests.post(OPENAI_API_URL, headers=HEADERS, json=payload)
    response.raise_for_status()
    result = response.json()
    synonyms = result.get("choices", [])[0]["message"]["content"].split(",")
    return [syn.strip() for syn in synonyms]


# Iterate through entities and update synonyms
entities = data["assets"].get("entities", [])
for entity in entities:
    sublists = entity.get("list", {}).get("sublists", [])
    for sublist in sublists:
        list_key = sublist.get("listKey", "")
        if list_key:
            synonyms = generate_synonyms(list_key)
            for synonym_entry in sublist.get("synonyms", []):
                if synonym_entry.get("language") == "en-us":
                    existing_values = synonym_entry.get("values", [])
                    synonym_entry["values"] = list(set(existing_values + synonyms))

# Save the updated JSON
with open("Updated_NewCLU_Testing.json", "w", encoding="utf-8") as outfile:
    json.dump(data, outfile, indent=4, ensure_ascii=False)

print("Synonyms have been added and the file has been updated.")
