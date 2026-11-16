## Auto QQ Interactive BOT

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-orange.svg)
![NapCat](https://img.shields.io/badge/NapCat-OneBot%2011-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

This is an intelligent QQ chatbot powered by Ollama (Local or Cloud-based Large Language Models). It establishes a connection with the NapCat framework via the Python WebSocket module, providing low-latency and highly flexible interactions for group chat entertainment and private messaging.

---

## BOT Features

* Powered by the Ollama framework, it supports various mainstream open-source models (Llama 3, Qwen, Gemma，GPT), ensuring privacy and remaining free.
* Utilizes the WebSocket protocol for seamless communication with NapCat.
* Supports multiple interaction modes, including group chat "@" mentions, keyword triggers, and private messaging.
* The bot is written in pure Python, allowing for easy integration of custom plugins or additional functionalities.

---

## Tech Stack

* **Core Engine**: [Ollama](https://ollama.com/) (Local LLM Engine)
* **Bot Framework**: [NapCatQQ](https://github.com/NapNeko/NapCatQQ) (Based on OneBot 11 standard)
* **Language**: Python 3.8+
* **Protocol**: WebSocket (Client)

---

## How To Start

### 1. Prerequisites
* Install and run [Ollama](https://ollama.com/). Pull a model using: `ollama pull [model_name]` (Ensure the model name matches the one specified in your Python script).
* Deploy [NapCatQQ](https://github.com/NapNeko/NapCatQQ) and enable the **Forward WebSocket Service** (Default port: `3001`).

### 2. Installation /// Execution
```bash
# Clone the repository

cd YOUR_REPO_NAME
git clone https://github.com/yunjiege2-debug/QQbot-for-chatting-

# Install dependencies
pip install -r requirements.txt

# Run the bot
python main.py
