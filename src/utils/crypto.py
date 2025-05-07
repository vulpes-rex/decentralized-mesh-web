from cryptography.fernet import Fernet
from nacl.public import Box, PrivateKey, PublicKey
import os

class CryptoHandler:
    def __init__(self):
        self.fernet = Fernet(Fernet.generate_key())
        self.private_key = PrivateKey.generate()
        
    def encrypt_data(self, data):
        if isinstance(data, str):
            data = data.encode()
        return self.fernet.encrypt(data)
        
    def decrypt_data(self, encrypted_data):
        return self.fernet.decrypt(encrypted_data)
        
    def generate_keypair(self):
        private_key = PrivateKey.generate()
        public_key = private_key.public_key
        return private_key, public_key