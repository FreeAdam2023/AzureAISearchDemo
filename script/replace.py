"""
@Time ： 2024-12-17
@Auth ： Adam Lyu
"""

import json

# 定义输入和输出文件路径
input_file_path = 'NewCLU_Testing.json'
output_file_path = 'NewCLU_Testing_modified.json'

# 读取 JSON 文件
with open(input_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# 递归函数：替换 "compositionSetting" 的值
def replace_composition_setting(obj):
    if isinstance(obj, dict):  # 如果是字典
        for key, value in obj.items():
            if key == "compositionSetting" and value == "requireExactOverlap":
                obj[key] = "returnLongestOverlap"  # 替换值
            else:
                replace_composition_setting(value)  # 递归处理子对象
    elif isinstance(obj, list):  # 如果是列表
        for item in obj:
            replace_composition_setting(item)  # 递归处理列表中的元素

# 调用函数进行替换
replace_composition_setting(data)

# 保存修改后的 JSON 文件
with open(output_file_path, 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

print(f"修改后的文件已保存到: {output_file_path}")
