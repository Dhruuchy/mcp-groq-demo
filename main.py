import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage

from database import setup_database
from agent import create_agent_executor

def main():
    # Load environment variables from .env file (for GROQ_API_KEY)
    load_dotenv()

    # Ensure the database is ready
    print("Setting up database...")
    setup_database()

    # Create our agent executor
    print("Creating AI agent...")
    agent_executor = create_agent_executor()
    print("Agent is ready! Ask me to list, find, or add users.")
    print("Type 'exit' to end the conversation.")

    # Store the conversation history
    chat_history = []

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        # Invoke the agent with the user's input and chat history
        response = agent_executor.invoke(
            {"input": user_input, "chat_history": chat_history}
        )

        # Add the interaction to our history
        chat_history.append(HumanMessage(content=user_input))
        chat_history.append(AIMessage(content=response["output"]))

        print(f"\nAgent: {response['output']}")


if __name__ == "__main__":
    main()