import shutil
import zipfile
from datetime import datetime
from pathlib import Path


class BackupManager:
    """
    Класс для создания и восстановления зашифрованных резервных копий файлов.

    :param encryptor: Объект для шифрования и дешифрования файлов.
    """
    def __init__(self, encryptor):
        self.encryptor = encryptor
        self.source_dir = Path("Data/source")
        self.backup_dir = Path("Data/Backup")
        self.restore_dir = Path("Data/Restore")

    def create_backup(self):
        """
        Создает резервную копию зашифрованных файлов.

        :return: Название созданного архива.
        """
        # Создаем временную папку для зашифрованных файлов
        temp_dir = self.backup_dir / "temp"
        temp_dir.mkdir(parents=True, exist_ok=True)

        # Шифруем файлы из исходной папки
        for file_path in self.source_dir.glob("**/*"):
            if file_path.is_file():
                relative_path = file_path.relative_to(self.source_dir)
                encrypted_file_path = temp_dir / relative_path
                encrypted_file_path.parent.mkdir(parents=True, exist_ok=True)
                self.encryptor.encrypt_file(file_path, encrypted_file_path)

        # Создаем архив из зашифрованных файлов
        archive_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        archive_path = self.backup_dir / archive_name

        with zipfile.ZipFile(archive_path, 'w') as archive:
            for file_path in temp_dir.glob("**/*"):
                if file_path.is_file():
                    archive.write(file_path, arcname=file_path.relative_to(temp_dir))

        # Удаляем временную папку
        shutil.rmtree(temp_dir)

        print(f"Создана резервная копия: {archive_path}")

        return archive_name

    def restore_backup(self, archive_name):
        """
        Восстанавливает резервную копию, расшифровывает файлы и создает новый архив с расшифрованными данными.

        :param archive_name: Название архива для восстановления.
        :return: Название созданного архива с расшифрованными данными.
        """
        # Создаем временную папку для разархивированных файлов
        temp_dir = self.restore_dir / "temp"
        temp_dir.mkdir(parents=True, exist_ok=True)

        archive_path = self.backup_dir / archive_name

        # Разархивируем файлы
        with zipfile.ZipFile(archive_path, 'r') as archive:
            archive.extractall(temp_dir)

        # Дешифруем файлы и сохраняем в временной папке
        for file_path in temp_dir.glob("**/*"):
            if file_path.is_file():
                relative_path = file_path.relative_to(temp_dir)
                decrypted_file_path = temp_dir / relative_path
                self.encryptor.decrypt_file(file_path, decrypted_file_path)

        # Создаем архив из расшифрованных файлов
        restored_archive_name = archive_name.replace(".zip", "_restored.zip")
        restored_archive_path = self.restore_dir / restored_archive_name

        with zipfile.ZipFile(restored_archive_path, 'w') as archive:
            for file_path in temp_dir.glob("**/*"):
                if file_path.is_file():
                    archive.write(file_path, arcname=file_path.relative_to(temp_dir))

        # Удаляем временную папку
        shutil.rmtree(temp_dir)

        print(f"Резервная копия восстановлена: {restored_archive_path}")

        return restored_archive_name
