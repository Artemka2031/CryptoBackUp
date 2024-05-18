import os
import shutil
import zipfile
from datetime import datetime
from pathlib import Path


class BackupManager:
    def __init__(self, encryptor):
        self.encryptor = encryptor

    def backup_files(self, source_dir, backup_root_dir):
        source_dir = Path(source_dir)
        backup_root_dir = Path(backup_root_dir)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_zip_path = backup_root_dir / f"{source_dir.name}_{timestamp}.zip"

        with zipfile.ZipFile(backup_zip_path, 'w') as zipf:
            for file_path in source_dir.glob('*'):
                if file_path.is_file():
                    encrypted_file_name = f"{file_path.stem}.enc{file_path.suffix}"
                    encrypted_file_path = file_path.parent / encrypted_file_name
                    self.encryptor.encrypt_file(str(file_path), str(encrypted_file_path))
                    zipf.write(str(encrypted_file_path), arcname=encrypted_file_name)
                    os.remove(str(encrypted_file_path))
                    print(f"File {file_path.name} encrypted and added to backup as {encrypted_file_name}")

        return backup_zip_path

    def restore_files(self, backup_zip, restore_root_dir):
        backup_zip = Path(backup_zip)
        restore_root_dir = Path(restore_root_dir)
        restored_zip_path = restore_root_dir / f"{backup_zip.stem}_restored.zip"
        temp_dir = Path(restore_root_dir / "temp")
        temp_dir.mkdir(parents=True, exist_ok=True)

        try:
            with zipfile.ZipFile(backup_zip, 'r') as zipf:
                zipf.extractall(path=temp_dir)
                print(f"Extracted files to {temp_dir}")

                with zipfile.ZipFile(restored_zip_path, 'w') as restored_zip:
                    for file_path in temp_dir.glob('*'):
                        if file_path.suffix == '.enc':
                            try:
                                original_extension = file_path.stem[-4:] if file_path.stem.endswith('.enc') else ''
                                decrypted_file_name = f"{file_path.stem[:-4]}{original_extension}"
                                decrypted_file_path = file_path.with_name(decrypted_file_name)
                                self.encryptor.decrypt_file(str(file_path), str(decrypted_file_path))
                                restored_zip.write(str(decrypted_file_path), arcname=decrypted_file_name)
                                os.remove(str(file_path))
                                os.remove(str(decrypted_file_path))
                                print(
                                    f"File {file_path.name} decrypted and added to restored archive as {decrypted_file_name}")
                            except Exception as e:
                                print(f"Error decrypting {file_path.name}: {e}")
            shutil.rmtree(temp_dir)  # Cleanup temporary directory
            print(f"Restored files are zipped in {restored_zip_path}")
            return restored_zip_path
        except FileNotFoundError:
            print(f"Backup zip file {backup_zip} not found.")
            return None
        except zipfile.BadZipFile:
            print(f"File {backup_zip} is not a zip file or it is corrupted.")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
