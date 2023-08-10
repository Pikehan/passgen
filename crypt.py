import cryptography
from cryptography.fernet import Fernet


def encrypt_(original):
    key = Fernet.generate_key()
    fernet = Fernet(key)

    encrypted = fernet.encrypt(original.encode("utf-8"))

    with open('data', 'wb') as encrypted_file:
        encrypted_file.write(key+encrypted)


def decrypt_():
    with open('data', 'rb') as datafile:
        key = datafile.read(44)
        data = datafile.read()

    try:
        fernet = Fernet(key)
    except ValueError:
        print("Corrupted key")
        return "[]"

    try:
        return fernet.decrypt(data).decode("utf-8")

    except (cryptography.fernet.InvalidToken, TypeError):
        print("Invalid Token")

