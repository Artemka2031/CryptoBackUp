import argparse

from BackupManager import BackupManager
from FileEncryptor import FileEncryptor


def main():
    """
    Основная функция для работы с резервными копиями и восстановлением файлов с шифрованием.

    Использует argparse для обработки аргументов командной строки.

    Аргументы командной строки:
    - action: Действие, которое необходимо выполнить ('backup' для создания резервной копии или 'restore' для восстановления).
    - --password: Пароль для шифрования/дешифрования файлов.
    - --archive: Название архива для восстановления (требуется только для действия 'restore').
    """
    parser = argparse.ArgumentParser(description="Резервная копия и восстановление файлов с шифрованием")
    parser.add_argument("action", choices=["backup", "restore"], help="Действия для выполнения: 'backup' или 'restore'")
    parser.add_argument("--password", required=True, help="Пароль для encryption/decryption")
    parser.add_argument("--archive", help="Имя архива для восстановления (требуется только для действия 'restore')")

    args = parser.parse_args()

    encryptor = FileEncryptor(args.password)
    manager = BackupManager(encryptor)

    if args.action == "backup":
        archive_name = manager.create_backup()
        print(f"Успешно создан архив: {archive_name}")
    elif args.action == "restore":
        if not args.archive:
            print("Ошибка: --archive обязательный атрибут для действия 'restore'")
            return
        restored_archive_name = manager.restore_backup(args.archive)
        print(f"Успешно восстановлен архив: {restored_archive_name}")


if __name__ == "__main__":
    main()
