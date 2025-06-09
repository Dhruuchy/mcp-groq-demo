from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor

# Tool Imports
from tools import list_all_users, get_user_details, add_new_user, greet_user, update_user_details, delete_user


def create_agent_executor():
    """
    Creates the agent by binding the LLM to the tools and creating the executor.
    """
    # 1. Define the list of tools the agent can use
    tools = [list_all_users, get_user_details, add_new_user, greet_user, update_user_details, delete_user]

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a database assistant. Your most important task is to "
                "distinguish between creating a NEW user and updating an "
                "EXISTING one.\n\n"
                "RULES:\n"
                "1. If the user's query contains words like 'update', 'modify', "
                "'change', or 'edit', you MUST use the `update_user_details` tool.\n"
                "2. Under these circumstances (update, modify, change, edit), "
                "you are FORBIDDEN from using the `add_new_user` tool.\n"
                "3. If you need more information to use a tool (like an email "
                "address), you MUST ask the user for it.\n"
                "4. Do not make up answers. If a tool fails, report the error "
                "and stop.",
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    # 3. Choose the LLM. We use Groq for its speed.
    llm = ChatGroq(model_name="llama3-70b-8192", temperature=0)

    # 4. Create the agent by binding the tools to the LLM
    agent = create_tool_calling_agent(llm, tools, prompt)

    # 5. Create the Agent Executor, which is the runtime for the agent.
    agent_executor = AgentExecutor(
        agent=agent, tools=tools, verbose=True
    )  # verbose=True lets us see the agent's thoughts

    return agent_executor