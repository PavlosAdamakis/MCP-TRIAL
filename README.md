# MCP Test Agent

This project is a lightweight, modular AI assistant framework based on the **Model Content Protocol (MCP)**. It simulates agent-to-agent communication where messages are passed in a structured way between components like tools and user interfaces.

---

##  Features

* 🧠 **MCP (Model Content Protocol)**: Enables structured message passing between agents.
* 🌤️ **Weather Tool**: Get current weather info for any city using wttr.in.
* 💻 **Shell Tool**: Run basic shell commands.
* 📊 **Excel Tool**: Upload and clean Excel files with natural language instructions.
* 🧠 **Store Data Tool**: Log notes, metrics, and structured content.
* 📧 **Gmail Tool** *(Optional)*: Compose email drafts (can be expanded).
* 💬 **Interactive Web UI**: Talk to the assistant directly from your browser.

---

##  Why MCP?

MCP stands for **Model Content Protocol**. It simulates a structured, agent-like messaging system that mimics AI-to-AI communication. In this project:

* The Web UI acts as **WebUser**.
* Messages are dispatched to **OpsAgent**.
* Tools return results as structured `Message` objects.

This design allows you to plug and play new tools easily and reuse the messaging layer across different agents or systems.

---

##  How to Use

### 1. Clone & Set Up

```bash
cd mcp-test
uv venv
source .venv/bin/activate  # or use uv shell on Windows
uv pip install -r requirements.txt
```

### 2. Run the App

```bash
uvicorn ui.server:app --reload
```

Open your browser at [http://localhost:8000](http://localhost:8000)

---

##  Commands You Can Try

### Weather

```
weather in Tokyo
weather Paris
```

### Shell

```
echo Hello World
```

### Excel

1. Upload an Excel file with your data
2. Enter instruction like:

```
tidy this up
clean it and sort by type
```

3. You'll get a cleaned file to download 

### Store Data

```
model=GPT-4, accuracy=94%, use-case=chatbot
note: response time was slow
```

---

##  Project Structure

```
mcp-test/
├── agents/
│   └── ops_agent.py
├── tools/
│   ├── shell.py
│   ├── weather.py
│   ├── excel.py
│   └── store_data.py
├── mcp/
│   └── protocol.py
├── ui/
│   ├── server.py
│   └── templates/
│       └── index.html
├── main.py (optional)
├── requirements.txt
└── README.md
```

---

##  Inspiration

Inspired by [Shaw Talebi](https://www.youtube.com/watch?v=N3vHJcHBS-w)'s demonstration of AI routing and tool use with agents.

---

##  Future Ideas

* Add email writing support with GPT or templates
* Logging with MongoDB or SQLite
* GPT-based tool routing with `tool_router`

---

##  Maintainer

Built by [@PavlosAdamakis](https://github.com/PavlosAdamakis) as a demonstration of MCP-based personal AI tooling for real-world use cases.

---

Ready to run and experiment with your own AI-powered assistant 
