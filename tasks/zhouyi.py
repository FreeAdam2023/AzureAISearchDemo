"""
@Time ： 2025-03-12
@Auth ： Adam Lyu
"""


def binary_to_lotto_numbers(binary_str):
    # 将 6 位二进制数转换为十进制数
    decimal_value = int(binary_str, 2)

    # 用一个集合确保没有重复
    numbers = set()

    # 通过取模来映射到 1-50 之间的号码，直到找到 7 个独特号码
    while len(numbers) < 7:
        num = (decimal_value % 50) + 1  # 映射到 1-50 的范围
        numbers.add(num)
        decimal_value = (decimal_value * 3 + 7) % 64  # 用简单的增量变化避免重复
    return sorted(numbers)


# 示例：6 位二进制数 '101001'
binary_input = "001000"
lotto_numbers = binary_to_lotto_numbers(binary_input)
print(lotto_numbers)