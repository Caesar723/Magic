import yaml, os 
import numpy as np



def read_yaml(file):
    with open(file, 'r', encoding="utf-8") as f:
        data = yaml.safe_load( f )
    return data 


def save_yaml(file, data):
    with open(file, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f)


def read_symbol_link(link_path):
    link_dir = os.path.split(link_path)[0] 
    link_file = os.readlink(link_path) 
    return os.path.join(link_dir, link_file) 


def set_symbol_link(link_file, symbol, overwrite=True):
    link_dir, fn = os.path.split(link_file)
    link_path = os.path.join(link_dir, symbol)
    if os.path.islink(link_path) and overwrite:
        os.remove(link_path)
    os.symlink(fn, link_path) 





import hashlib
import base64

def hash_string(string, length=10):
    # Generate a SHA-256 hash
    hash_obj = hashlib.sha256(string.encode())
    # Encode in Base64 and make it URL-safe
    hash_b64 = base64.urlsafe_b64encode(hash_obj.digest()).decode()
    # Trim to desired length
    return hash_b64[:length]



if __name__ == "__main__":
    pass