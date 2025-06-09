from langchain_core.tools import tool
from pydantic import BaseModel, Field
import sqlite3
from typing import Optional

# --- Schemas ---

class GetUserDetailsInput(BaseModel):
    name: str = Field(description="The name of the user to search for.")

class AddUserInput(BaseModel):
    name: str = Field(description="The full name of the new user.")
    email: str = Field(description="The unique email address for the new user.")

class UpdateUserInput(BaseModel):
    name: str = Field(description="The name of the user to be updated.")
    new_name: Optional[str] = Field(
        default=None, description="The user's new name. (Optional)"
    )
    new_email: Optional[str] = Field(
        default=None, description="The user's new email address. (Optional)"
    )

class DeleteUserInput(BaseModel):
    name: str = Field(description="The name of the user to be deleted.")


# --- Tools ---

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
    """
    Use this tool ONLY when the user explicitly asks to 'find', 'get', 'see',
    or 'look up' a specific user's details. This is a read-only operation.
    Do NOT use this as a preliminary step for updating or deleting a user.
    """
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, email FROM users WHERE name = ?", (name,))
    user = cursor.fetchone()
    conn.close()
    if not user:
        return f"No user found with the name '{name}'."
    return f"User Details: Name={user[0]}, Email={user[1]}"


@tool("add_new_user", args_schema=AddUserInput)
def add_new_user(name: str, email: str) -> str:
    """
    Use this tool to add a completely new user to the database. This should only
    be used when the user does not already exist in the system.
    """
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


@tool("update_user_details", args_schema=UpdateUserInput)
def update_user_details(
    name: str, new_name: Optional[str] = None, new_email: Optional[str] = None
) -> str:
    """
    Use this tool to modify the details (like name or email) of an *existing* user.
    The user is identified by their current name.
    """
    if not new_name and not new_email:
        return "Error: You must provide a new name or a new email to update."
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    set_clauses = []
    params = []
    if new_name:
        set_clauses.append("name = ?")
        params.append(new_name)
    if new_email:
        set_clauses.append("email = ?")
        params.append(new_email)
    params.append(name)
    query = f"UPDATE users SET {', '.join(set_clauses)} WHERE name = ?"
    try:
        cursor.execute(query, params)
        if cursor.rowcount == 0:
            return f"Error: No user found with the name '{name}'."
        conn.commit()
        return f"Successfully updated user '{name}'."
    except sqlite3.IntegrityError:
        return f"Error: The email '{new_email}' already exists for another user."
    finally:
        conn.close()


@tool("delete_user", args_schema=DeleteUserInput)
def delete_user(name: str) -> str:
    """
    Use this tool to permanently delete an existing user from the database.
    The user is identified by their name. This action cannot be undone.
    """
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE name = ?", (name,))
    if cursor.rowcount == 0:
        return f"Error: No user found with the name '{name}' to delete."
    conn.commit()
    return f"User '{name}' has been successfully deleted."


@tool(return_direct=True)
def greet_user() -> str:
    """
    Provides a greeting and explains the agent's capabilities.
    Use this tool when the user says hello, hi, or asks what you can do.
    """
    return (
        "Hello! I am a database management assistant with full CRUD capabilities.\n"
        "I can help you with the following tasks:\n"
        "- List all users\n"
        "- Get details for a specific user\n"
        "- Add a new user\n"
        "- Update an existing user's name or email\n"
        "- Delete a user"
    )