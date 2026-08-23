import yaml, os 
import numpy as np

import hashlib
import base64


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

def save_metadata(data, file, header=None):
    ''' 保存metadata数据到文件  

    Args:
        data (list): metadata数据
        file (str): 保存文件名
        header (list): 保存的 列名顺序  
    '''
    if header is None:
        header = data[0].keys()
    with open(file, "w", encoding="utf-8") as f:
        f.write( '|'.join(header) + "\n" ) 
        for d in data:
            d = [ str( d.get(k, "") ) for k in header ]
            line = "|".join([ v.replace("|"," ") for v in d ])
            f.write( line + "\n" ) 


def read_metadata(file,header=None):
    ''' 读取metadata  

    Args:
        file (str): metadata文件  
        
    Returns:
        list[ dict ]: metadata数据，
        list: 列名
    '''
    with open(file, "r", encoding="utf-8") as f:
        lines = f.readlines() 

    data = []
    if header is None:
        header = lines[0].strip().split("|") 
        lines = lines[1:]

    for line in lines:
        line = line.strip()
        if line == "": continue
        d = line.split("|") 
        data.append( {k:v for k,v in zip(header, d)} ) 
    return data, header 




def hash_string(string, length=10):
    # Generate a SHA-256 hash
    hash_obj = hashlib.sha256(string.encode())
    # Encode in Base64 and make it URL-safe
    hash_b64 = base64.urlsafe_b64encode(hash_obj.digest()).decode()
    # Trim to desired length
    return hash_b64[:length]



if __name__ == "__main__":
    pass