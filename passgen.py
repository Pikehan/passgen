import secrets


def generate_password(pwd_length, character):
    return ''.join(secrets.choice(character) for _ in range(pwd_length))
