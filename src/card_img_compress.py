
from PIL import Image
import os


ORGPATH=os.path.dirname(os.path.abspath(__file__))

def compress_all_img():
    path_types=[
        "cards/creature",
        "cards/Instant",
        "cards/land",
        "cards/sorcery",
    ]
    for path_type in path_types:
        for folder in os.listdir(f"{ORGPATH}/{path_type}"):
            if folder ==".DS_Store":
                continue
            files=os.listdir(f"{ORGPATH}/{path_type}/{folder}")
            
            if "compress_img" in files:
                continue
            preprocess_image()
            # for file in os.listdir(f"{ORGPATH}/{path_type}/{folder}"):
            #     if file.endswith(".png"):
            #         preprocess_image(f"{ORGPATH}/{path_type}/{folder}/{file}", f"{ORGPATH}/{path_type}/{folder}/{file}", (50, 50))
def preprocess_image(input_path: str, output_path: str, size=(50, 50)):
    """预处理图片：调整大小并保存为压缩格式"""
    image = Image.open(input_path)
    image = image.resize(size)  # 调整大小
    image.save(output_path, format="JPEG", quality=80)  # 保存为JPEG并压缩

if __name__=="__main__":
    compress_all_img()
