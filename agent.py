# agent.py
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor

# Import the tools we defined
from tools import list_all_users, get_user_details, add_new_user, greet_user


def create_agent_executor():
    """
    Creates the agent by binding the LLM to the tools and creating the executor.
    """
    # 1. Define the list of tools the agent can use
    tools = [list_all_users, get_user_details, add_new_user, greet_user]

    # We are creating a generic prompt template that is not tied to a specific
    # model like OpenAI. LangChain will adapt this for Groq's Llama 3.
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant that can manage a user database.\n"
                "1. Your first priority is to understand the user's goal.\n"
                "2. Look at your tools and see if one can help.\n"
                "3. If the user wants to use a tool but has NOT provided all the "
                "necessary information (like a name or email), you MUST ask for "
                "the missing information first.\n"
                "4. Do NOT attempt to call a tool with incomplete information.\n"
                "5. Only after you have all the required arguments should you "
                "call the tool.",
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
        agent=agent, tools=tools, verbose=False
    )  # verbose=True lets us see the agent's thoughts

    return agent_executor