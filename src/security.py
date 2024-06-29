from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization,hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from base64 import b64encode, b64decode
import binascii
import re





class Security:

    def __init__(self) -> None:
        self.private_key,self.public_key=self.generate_keys()
        self.public_key_pem = self.export_public_key()

    def generate_keys(self):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        return private_key, public_key

    # 导出公钥
    def export_public_key(self):
        pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return pem

    # 使用私钥解密消息
    def decrypt_message(self,encrypted_message):
        encrypted_message=b64decode(encrypted_message)
        decrypted_message = self.private_key.decrypt(
            encrypted_message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted_message.decode()
    
    def decrypt_with_aes(self,encrypted_text):
        key_base64,iv_base64,encrypted_data_base64=encrypted_text.split(";")
        
        
        # 初始化解密器
        encrypted_data = b64decode(encrypted_data_base64)
        iv = b64decode(iv_base64)
        key= b64decode(key_base64)

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

        # 将解密后的数据从字节转换为字符串
        decrypted_str = decrypted_data.decode('utf-8').replace("\t","")
        
        cleaned_str = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', decrypted_str)
        return cleaned_str
        
    
    def decrypt_base64(self,word):
        return binascii.unhexlify(word)