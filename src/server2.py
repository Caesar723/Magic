import json


a="{'ll':ll}"
# 假设这是你要转换的字典
my_dict = {
    "name": a,
    "age": 30,
    "city": "New York"
}

# 将字典序列化成JSON格式的字符串
json_str = json.dumps(my_dict)

print(json.loads(json_str))
# 将JSON字符串编码成字节
json_bytes = json_str.encode('utf-8')  # utf-8是一种常见的编码格式

# 打印结果以验证

