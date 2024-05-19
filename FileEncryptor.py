import base64
import secrets

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


class FileEncryptor:
    """
    Класс для шифрования и дешифрования файлов.

    :param password: Пароль для генерации ключа.
    :param salt_size: Размер соли в байтах.
    :param load_existing_salt: Загрузка существующей соли из файла.
    :param save_salt: Сохранение соли в файл.
    """

    def __init__(self, password, salt_size=16, load_existing_salt=True, save_salt=True):
        self.password = password
        self.salt_size = salt_size
        self.load_existing_salt = load_existing_salt
        self.save_salt = save_salt
        self.key = self.generate_key()

    @staticmethod
    def generate_salt(size=16):
        """
        Генерация случайной соли.

        :param size: Размер соли в байтах.
        :return: Случайная соль.
        """
        return secrets.token_bytes(size)

    @staticmethod
    def load_salt():
        """
        Загрузка соли из файла.

        :return: Соль, загруженная из файла, или None, если файл не найден.
        """
        try:
            with open("salt.salt", "rb") as salt_file:
                return salt_file.read()
        except FileNotFoundError:
            return None

    def derive_key(self, salt):
        """
        Производная ключа из пароля и соли.

        :param salt: Соль для ключа.
        :return: Производный ключ.
        """
        kdf = Scrypt(salt=salt, length=32, n=2 ** 14, r=8, p=1)
        return kdf.derive(self.password.encode())

    def generate_key(self):
        """
        Генерация ключа для шифрования.

        :return: Ключ для шифрования.
        :raises ValueError: Если файл соли не найден при загрузке существующей соли.
        """
        if self.load_existing_salt:
            salt = self.load_salt()
            if not salt:
                raise ValueError("Salt file not found")
        else:
            salt = self.generate_salt(self.salt_size)

        if self.save_salt and not self.load_existing_salt:
            with open("salt.salt", "wb") as salt_file:
                salt_file.write(salt)

        return base64.urlsafe_b64encode(self.derive_key(salt))

    def encrypt_file(self, source_file, dest_file):
        """
        Шифрование файла.

        :param source_file: Путь к исходному файлу для шифрования.
        :param dest_file: Путь к зашифрованному файлу.
        """
        f = Fernet(self.key)
        with open(source_file, 'rb') as file:
            file_data = file.read()
        encrypted_data = f.encrypt(file_data)
        with open(dest_file, 'wb') as file:
            file.write(encrypted_data)

    def decrypt_file(self, source_file, dest_file):
        """
        Дешифрование файла.

        :param source_file: Путь к зашифрованному файлу.
        :param dest_file: Путь к расшифрованному файлу.
        """
        f = Fernet(self.key)
        with open(source_file, 'rb') as file:
            encrypted_data = file.read()
        decrypted_data = f.decrypt(encrypted_data)
        with open(dest_file, 'wb') as file:
            file.write(decrypted_data)
