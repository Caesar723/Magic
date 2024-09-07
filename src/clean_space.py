import os
import re

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 使用正则表达式匹配并修改
    pattern1 = r'(self\.\w+:\s*str\s*=\s*"[^"]*)\s+"'
    modified_content, count1 = re.subn(pattern1, r'\1"', content)
    
    pattern2 = r'(\w+/\w+/[^/]+)\s{2}/'
    modified_content, count2 = re.subn(pattern2, r'\1/', modified_content)
    
    count = count1 + count2
    if count > 0:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(modified_content)
        print(f"修改了 {file_path} 中的 {count} 处")

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                process_file(file_path)

# 替换为您的pycards文件夹的实际路径
pycards_directory = "/Users/xuanpeichen/Desktop/code/python/openai/src/pycards"
process_directory(pycards_directory)