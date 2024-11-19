<p align="center">
    <img src="https://media.discordapp.net/attachments/1036960627127762944/1306556988418822194/image.png?ex=673d0844&is=673bb6c4&hm=c274bbfaa69e33ebcfdae5d328272be93098f7b7bbbd118796af90381fcb4956&=&format=webp&quality=lossless&width=662&height=662" align="center" width="30%">
</p>
<h1 align="center">BOT_DISCORD</h1>
<p align="center">
	<em><code>❯ A Discord bot to decrypt Chrome-stored passwords from uploaded files</code></em>
</p>
<p align="center">
	<img src="https://img.shields.io/github/license/Cronix2/bot_discord?style=default&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/Cronix2/bot_discord?style=default&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/Cronix2/bot_discord?style=default&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/Cronix2/bot_discord?style=default&color=0080ff" alt="repo-language-count">
</p>

---

## 🔗 Table of Contents

- [📍 Overview](#-overview)
- [👾 Features](#-features)
- [📁 Project Structure](#-project-structure)
- [🚀 Getting Started](#-getting-started)
  - [☑️ Prerequisites](#%EF%B8%8F-prerequisites)
  - [⚙️ Installation](#%EF%B8%8F-installation)
  - [🤖 Usage](#-usage)
- [🔰 Contributing](#-contributing)
- [🎗 License](#-license)
- [🙌 Acknowledgments](#-acknowledgments)

---

## 📍 Overview

This Discord bot is designed to decrypt Chrome-stored passwords from a `.zip` file containing critical files (`LOGIN_DATA`, `Local_State`, and a master decryption key). The bot automatically extracts and decrypts these files, outputting the credentials in readable `.txt` and `.xlsx` formats. The bot can process new files uploaded via Discord webhooks, and a `/decrypt_file` command allows manual decryption of the last uploaded zip file.

---

## 👾 Features

- **Automated Decryption**: Decrypts Chrome passwords from uploaded zip files containing login data.
- **Two Output Formats**: Decrypted data is returned as a text file and Excel spreadsheet for easy review.
- **Webhook Integration**: Automatically processes new zip files sent via webhooks.
- **Command-Based Decryption**: Use `/decrypt_file` to trigger decryption on the latest uploaded file.
- **Keep-Alive Monitoring**: Uses `keep_alive.py` to ensure the bot remains active by checking server status.

---

## 📁 Project Structure

```sh
└── bot_discord/
    ├── LICENSE
    ├── main.py            # Primary code for decryption and file processing
    ├── bot.py             # Bot setup and webhook message handling
    ├── keep_alive.py      # Script to maintain bot uptime on the server
    └── requirements.txt   # Required dependencies
```

---

## 🚀 Getting Started

### ☑️ Prerequisites

- **Python**: Ensure Python is installed on your system.
- **Pip**: Required to install dependencies.

### ⚙️ Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/Cronix2/bot_discord.git
   cd bot_discord
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

### 🤖 Usage

1. **Configure Bot Token**: Set up your Discord bot token in `bot.py` or a `.env` file.
2. **Run the Bot**: Start the bot by running:
   ```sh
   python bot.py
   ```
3. **Process Zip Files**: The bot will automatically detect zip files sent via Discord webhooks and decrypt credentials. Use the `/decrypt_file` command to manually decrypt the latest file.

---

## 🔰 Contributing

1. Fork the repository and create a new branch:
   ```sh
   git checkout -b feature-name
   ```
2. Make your changes, commit, and push the branch:
   ```sh
   git commit -m "Add feature X"
   git push origin feature-name
   ```
3. Open a pull request for review.

---

## 🎗 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 🙌 Acknowledgments

Special thanks to contributors and the Discord API community.
