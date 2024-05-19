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
    parser = argparse.ArgumentParser(description="Backup and restore files with encryption")
    parser.add_argument("action", choices=["backup", "restore"], help="Action to perform: 'backup' or 'restore'")
    parser.add_argument("--password", required=True, help="Password for encryption/decryption")
    parser.add_argument("--archive", help="Name of the archive to restore (required for 'restore' action)")

    args = parser.parse_args()

    encryptor = FileEncryptor(args.password)
    manager = BackupManager(encryptor)

    if args.action == "backup":
        archive_name = manager.create_backup()
        print(f"Created backup archive: {archive_name}")
    elif args.action == "restore":
        if not args.archive:
            print("Error: --archive is required for restore action")
            return
        restored_archive_name = manager.restore_backup(args.archive)
        print(f"Restored backup archive: {restored_archive_name}")

if __name__ == "__main__":
    main()
