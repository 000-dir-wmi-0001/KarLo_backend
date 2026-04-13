from cryptography.fernet import Fernet
import os

SECRET_KEY = os.getenv("MFA_ENCRYPTION_KEY") or Fernet.generate_key()
cipher = Fernet(SECRET_KEY)

def encrypt(data: str) -> str:
    return cipher.encrypt(data.encode()).decode()

def decrypt(data: str) -> str:
    return cipher.decrypt(data.encode()).decode()