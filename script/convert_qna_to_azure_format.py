import json
import csv

# 文件路径
input_file = "../data/testqnasCaseManagement.json"  # 输入 JSON 文件
output_file_en = "../result/testqnasCaseManagement_en_azure.tsv"  # 输出的英语 TSV 文件
output_file_fr = "../result/testqnasCaseManagement_fr_azure.tsv"  # 输出的法语 TSV 文件


# JSON 转 TSV 的函数（基于交替拆分）
def json_to_tsv_alternate(input_file, output_file_en, output_file_fr):
    with open(input_file, "r", encoding="utf-8") as infile:
        data = json.load(infile)

    en_rows = []
    fr_rows = []

    # 遍历 JSON 数据，交替分配到英语和法语
    for i, entry in enumerate(data):
        value = entry.get("value", {})
        answer = value.get("answer", "")
        questions = value.get("questions", [])
        metadata = "; ".join(
            [f"{key}:{value['metadata'].get(key)}" for key in value.get("metadata", {})]
        )

        # 每个问题创建一行
        for question in questions:
            if i % 2 == 0:  # 偶数索引 -> 英语
                en_rows.append([question, answer, metadata])
            else:  # 奇数索引 -> 法语
                fr_rows.append([question, answer, metadata])

    # 保存为 TSV 文件
    save_to_tsv(output_file_en, en_rows)
    save_to_tsv(output_file_fr, fr_rows)

    print(f"English TSV data saved to {output_file_en}")
    print(f"French TSV data saved to {output_file_fr}")


# 保存数据到 TSV
def save_to_tsv(output_file, rows):
    with open(output_file, "w", encoding="utf-8", newline="") as outfile:
        tsv_writer = csv.writer(outfile, delimiter="\t")
        # 写入表头
        tsv_writer.writerow(["Question", "Answer", "Metadata"])
        # 写入数据
        tsv_writer.writerows(rows)


# 执行转换
json_to_tsv_alternate(input_file, output_file_en, output_file_fr)
