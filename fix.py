import os
import re

# 定义要添加的 dtype
DEFAULT_DTYPE = "torch.float32"

# 正则表达式，用于匹配 torch.tensor(dtype=torch.float32) 函数调用
tensor_pattern = re.compile(r'torch\.tensor\((.*?)(\))', re.DOTALL)

# 正则表达式，用于匹配 dtype 参数
dtype_pattern = re.compile(r'dtype\s*=\s*[^,]+')

def add_dtype_to_tensor_call(file_path):
    """检查并修改文件中的torch.tensor(dtype=torch.float32)调用，确保有dtype参数"""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    modified = False
    matches = tensor_pattern.findall(content)

    # 查找所有torch.tensor(dtype=torch.float32)调用
    for match in matches:
        tensor_args = match[0].strip()  # 获取参数部分
        # 检查是否已经包含 dtype 参数
        if not dtype_pattern.search(tensor_args):
            # 如果没有dtype，补充 dtype=torch.float32
            new_tensor_args = tensor_args + (', dtype=torch.float32' if tensor_args else 'dtype=torch.float32')
            new_content = content.replace(f'torch.tensor({tensor_args}{match[1]}', f'torch.tensor({new_tensor_args}{match[1]}', dtype=torch.float32)
            content = new_content
            modified = True

    if modified:
        # 如果文件有修改，写回文件
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

def process_files_in_directory(directory):
    """遍历指定目录及子目录，处理所有.py文件"""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):  # 只处理.py文件
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")
                add_dtype_to_tensor_call(file_path)

if __name__ == "__main__":
    # 获取当前目录
    current_directory = os.getcwd()

    # 处理当前目录及其子目录中的所有.py文件
    process_files_in_directory(current_directory)
