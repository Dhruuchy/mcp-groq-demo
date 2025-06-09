# AI-Powered CRUD Agent

A demonstration of a powerful AI agent built using **Model-Centric Programming (MCP)**. This agent manages a user database through natural language commands, performing full CRUD (Create, Read, Update, Delete) operations.

> **Key Idea:**  
> Instead of complex if/else logic, a Large Language Model (LLM) from Groq acts as the reasoning engine. The LLM is given Python functions as "tools" and decides which to use, in what order, and with what arguments to fulfill your request.

---

## ✨ Features

- **Create:** Add new users to the database.
- **Read (All):** List all users currently in the database.
- **Read (Single):** Get details for a specific user by name.
- **Update:** Modify an existing user's name or email.
- **Delete:** Permanently remove a user from the database.
- **Conversational Greeting:** The agent can introduce itself and explain its capabilities.

---

## 🛠️ Technology Stack

- **Python 3.8+** — Core programming language
- **LangChain** — Framework for building the agent and managing the reasoning loop
- **Groq API (Llama 3)** — Provides the LLM "brain" with fast inference
- **SQLite** — Simple, file-based database for user info
- **Pydantic** — Structured schemas for tool arguments and data validation

---

## 🧠 How It Works: Model-Centric Programming

- **LLM as Orchestrator:**  
    The Llama 3 model is the "brain," receiving user prompts and tool descriptions.
- **Python Functions as Tools:**  
    Each CRUD operation (e.g., `add_user`, `delete_user`) is a Python function decorated with LangChain's `@tool`.
- **Docstrings as the API:**  
    The agent reads function docstrings (not code) to understand what each tool does, when to use it, and what arguments it needs. Well-written docstrings prevent tool confusion.
- **Agent Executor:**  
    LangChain's `AgentExecutor` manages the process: sends prompts to the LLM, parses decisions, calls Python tools, and returns results.

---

## 🚀 Setup and Installation

1. **Prerequisites:**  
     Ensure you have Python 3.8 or newer installed.

2. **Clone the Repository:**  
     ```sh
     git clone <repo-url>
     cd mcp-groq-demo
     ```

---

## 💬 Example Conversation

```text
You: hello

Agent: Hello! I am a database management assistant with full CRUD capabilities.
I can help you with the following tasks:

- List all users
- Get details for a specific user
- Add a new user
- Update an existing user's name or email
- Delete a user

You: add a user named Clark Kent with email clark@dailyplanet.com

Agent: User 'Clark Kent' was successfully added to the database.

You: list all users

Agent:
- Alice (alice@wonderland.io)
- Charlie (charlie@factory.com)
- Clark Kent (clark@dailyplanet.com)

You: can you update clark kent's email to superman@fortress.solitude

Agent: I have successfully updated the user 'Clark Kent'.

You: what are the details for clark kent?

Agent: User Details: Name=Clark Kent, Email=superman@fortress.solitude

You: please delete clark kent

Agent: User 'Clark Kent' has been successfully deleted.
```

---

## 📁 Project Structure

```
mcp-groq-demo
├── .env               # Stores secret keys (DO NOT COMMIT)
├── requirements.txt   # Python dependencies
├── database.py        # SQLite database setup and connection
├── tools.py           # Python functions (CRUD tools)
├── agent.py           # AI agent and system prompt configuration
└── main.py            # Main application entrypoint and CLI
```