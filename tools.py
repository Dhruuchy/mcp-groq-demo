from langchain_core.tools import tool
from pydantic import BaseModel, Field
import sqlite3

# --- Tool Argument Schemas ---
# Using Pydantic gives the AI structured information about what inputs are needed.

class GetUserDetailsInput(BaseModel):
    name: str = Field(description="The name of the user to search for.")

class AddUserInput(BaseModel):
    name: str = Field(description="The full name of the new user.")
    email: str = Field(description="The unique email address for the new user.")


# --- The Tools ---

@tool
def list_all_users() -> str:
    """Lists all users currently in the database."""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, email FROM users")
    users = cursor.fetchall()
    conn.close()
    if not users:
        return "There are no users in the database."
    return "\n".join([f"- {name} ({email})" for name, email in users])


@tool("get_user_details", args_schema=GetUserDetailsInput)
def get_user_details(name: str) -> str:
    """Gets the details for a single user by their name."""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, email FROM users WHERE name LIKE ?", (f"%{name}%",))
    user = cursor.fetchone()
    conn.close()
    if not user:
        return f"No user found with the name '{name}'."
    return f"User Details: Name={user[0]}, Email={user[1]}"


@tool("add_new_user", args_schema=AddUserInput)
def add_new_user(name: str, email: str) -> str:
    """Adds a new user to the database. Returns a success or error message."""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
        return f"User '{name}' was successfully added to the database."
    except sqlite3.IntegrityError:
        return f"Error: A user with the email '{email}' already exists."
    finally:
        conn.close()

@tool(return_direct=True)
def greet_user() -> str:
    """
    Provides a greeting and explains the agent's capabilities.
    Use this tool when the user says hello, hi, or asks what you can do.
    """
    return (
        "Hello! I am a user database management assistant.\n"
        "I can help you with the following tasks:\n"
        "- List all users\n"
        "- Find a specific user by name\n"
        "- Add a new user to the database"
    )