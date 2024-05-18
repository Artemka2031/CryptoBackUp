from BackupManager import BackupManager
from FileEncryptor import FileEncryptor
from pathlib import Path

if __name__ == "__main__":
    password = "strong_password_here"
    encryptor = FileEncryptor(password=password)
    backup_manager = BackupManager(encryptor)

    source_directory = Path("Data/Source")
    backup_root_directory = Path("Data/Backup")
    backup_zip_path = backup_manager.backup_files(source_directory, backup_root_directory)
    print(f"Backup created at {backup_zip_path}")

    restore_directory = Path("Data/Restore")
    if backup_zip_path.exists():
        restored_zip_path = backup_manager.restore_files(backup_zip_path, restore_directory)
        print(f"Files restored and saved in archive: {restored_zip_path}")
    else:
        print("Backup file does not exist.")
