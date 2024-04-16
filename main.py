import base64
import getpass
import secrets

import argparse
import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


def generate_salt(size=16):
    return secrets.token_bytes(size)


def load_salt():
    return open("salt.salt", "rb").read()


def derive_key(salt, password):
    kdf = Scrypt(salt=salt, length=32, n=2 ** 14, r=8, p=1)
    return kdf.derive(password.encode())


def generate_key(password, salt_size=16, load_existing_salt=False, save_salt=True):
    if load_existing_salt:
        salt = load_salt()
    elif save_salt:
        salt = generate_salt(salt_size)
        with open("salt.salt", "wb") as salt_file:
            salt_file.write(salt)

    derive_key = derive_key(salt, password)
    return base64.urlsafe_b64encode(derive_key)


def encrypt(filename, key):
    f = Fernet(key)

    with open(filename, 'rb') as file:
        file_data = file.read()

    encrypted_data = f.encrypt(file_data)

    with open(filename, 'wb') as file:
        file.write(encrypted_data)

    print('File encrypted')


def decrypt(filename, key):
    f = Fernet(key)

    with open(filename, 'rb') as file:
        encrypted_data = file.read()

    try:
        decrypted_data = f.decrypt(encrypted_data)
    except cryptography.fernet.InvalidToken:
        print('Invalid token')
        return

    with open(filename, 'wb') as file:
        file.write(decrypted_data)

    print('File decrypted')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Encrypt or decrypt files")
    parser.add_argument("file", help="File to encrypt or decrypt")
    parser.add_argument("-s", "--save-salt", help="If set, save salt to salt.salt", action="store_true", type=int)
    parser.add_argument("-e", "--encrypt", action="store_true", help="Encrypt file")
    parser.add_argument("-d", "--decrypt", action="store_true", help="Decrypt file")

    args = parser.parse_args()
    file = args.file

    password = ""

    if args.encrypt:
        password = getpass.getpass("Enter the password to encrypt the file: ")
    elif args.decrypt:
        password = getpass.getpass("Enter the password  you you used to encrypt the file: ")

    if args.salt_size:
        key = generate_key(password, salt_size=args.salt_size, save_salt=True)
    else:
        key = generate_key(password, load_existing_salt=True)

    encrypt_ = args.encrypt
    decrypt_ = args.decrypt

    if encrypt_ and decrypt_:
        raise TypeError("Plese only use one of --encrypt or --decrypt")
    elif encrypt_:
        encrypt(file, key)
    elif decrypt_:
        decrypt(file, key)
    else:
        raise TypeError("Please use --encrypt or --decrypt")

    if encrypt_:
        encrypt(file, key)
    elif decrypt_:
        decrypt(file, key)
