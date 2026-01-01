import os
import operator
from typing import Annotated, List, TypedDict, Union

from langchain.agents import Tool
from langchain_core.tools import tool
from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
    ToolMessage,
)
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition

# Conditional imports to handle missing dependencies gracefully during dev (though we expect them)
try:
    from pyspark.sql import SparkSession
except ImportError:
    SparkSession = None

try:
    import git
except ImportError:
    git = None

try:
    from langchain_community.tools import WikipediaQueryRun
    from langchain_community.utilities import WikipediaAPIWrapper
except ImportError:
    WikipediaQueryRun = None

# --- 1. Define Tools ---


@tool
def query_spark_sql(query: str) -> str:
    """Execute a SparkSQL query on the 'sales' table.
    The table has columns: id (int), product (string), amount (int), category (string).
    """
    if not SparkSession:
        return "Spark not available."

    spark = SparkSession.builder.appName("LangGraphDemo").getOrCreate()
    # Create sample data if not exists (for demo)
    if not spark.catalog.tableExists("sales"):
        data = [
            (1, "Widget A", 100, "Hardware"),
            (2, "Widget B", 200, "Hardware"),
            (3, "Service X", 150, "Software"),
        ]
        df = spark.createDataFrame(data, ["id", "product", "amount", "category"])
        df.createOrReplaceTempView("sales")

    try:
        result = spark.sql(query).toJSON().collect()
        return "\n".join(result)
    except Exception as e:
        return f"Error executing query: {e}"


@tool
def check_git_status() -> str:
    """Check the git status of the current repository."""
    if not git:
        return "GitPython not available."
    try:
        repo = git.Repo(search_parent_directories=True)
        return str(repo.git.status())
    except Exception as e:
        return f"Error checking git status: {e}"


def get_wikipedia_tool():
    if WikipediaQueryRun:
        api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=500)
        return WikipediaQueryRun(api_wrapper=api_wrapper)
    return None


# --- 2. Define State ---


class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]


# --- 3. Mock LLM (For Demo purposes if no key) ---
# In a real scenario, use ChatOpenAI or similar
from langchain_core.language_models import FakeListLLM


def run_demo():
    print("--- Starting LangGraph Demo ---")

    # Setup Tools
    tools = [query_spark_sql, check_git_status]
    wiki_tool = get_wikipedia_tool()
    if wiki_tool:
        tools.append(wiki_tool)

    # Use a Real LLM if Key exists, else Fake
    llm = None
    if os.environ.get("OPENAI_API_KEY"):
        from langchain_openai import ChatOpenAI

        print("Using ChatOpenAI")
        llm = ChatOpenAI(model="gpt-3.5-turbo").bind_tools(tools)
    else:
        print("No OPENAI_API_KEY found. Using Safe Mock LLM execution for demo.")
        # Faking a conversation flow:
        # 1. User asks to check git.
        # 2. Agent calls git tool.
        # 3. User asks to query spark.
        # 4. Agent calls spark tool.
        # This is hard with just FakeListLLM and tools binding logic.
        # For this demo, we will use a simple specialized node that just invokes tools
        # based on keywords if no LLM is present, effectively a "RuleBasedAgent".

    # --- Graph Construction ---
    builder = StateGraph(AgentState)

    # Agent Node
    def agent_node(state: AgentState):
        messages = state["messages"]
        last_message = messages[-1]

        # Logic for "RuleBasedAgent" if no real LLM
        if not llm:
            # If the last message was a ToolMessage, it means the tool just ran.
            # The agent should now consume that output and finish.
            if isinstance(last_message, ToolMessage):
                return {
                    "messages": [
                        AIMessage(
                            content=f"Tool execution completed. Output: {last_message.content}"
                        )
                    ]
                }

            content = last_message.content.lower()
            if "git" in content:
                print("  [Agent Decides]: Call check_git_status")
                return {
                    "messages": [
                        AIMessage(
                            content="",
                            tool_calls=[
                                {"name": "check_git_status", "args": {}, "id": "call_1"}
                            ],
                        )
                    ]
                }
            elif "spark" in content or "sales" in content:
                print("  [Agent Decides]: Call query_spark_sql")
                return {
                    "messages": [
                        AIMessage(
                            content="",
                            tool_calls=[
                                {
                                    "name": "query_spark_sql",
                                    "args": {"query": "SELECT * FROM sales"},
                                    "id": "call_2",
                                }
                            ],
                        )
                    ]
                }
            elif "wiki" in content:
                print("  [Agent Decides]: Call wikipedia")
                return {
                    "messages": [
                        AIMessage(
                            content="",
                            tool_calls=[
                                {
                                    "name": "wikipedia",
                                    "args": {"query": "LangChain"},
                                    "id": "call_3",
                                }
                            ],
                        )
                    ]
                }
            else:
                return {
                    "messages": [
                        AIMessage(
                            content="I am a demo bot. Ask me about git, spark, or wiki."
                        )
                    ]
                }

        # Real LLM logic
        response = llm.invoke(messages)
        return {"messages": [response]}

    builder.add_node("agent", agent_node)

    # Tool Node
    tool_node = ToolNode(tools)
    builder.add_node("tools", tool_node)

    # Edges
    builder.set_entry_point("agent")

    def should_continue(state: AgentState):
        last_message = state["messages"][-1]
        if isinstance(last_message, AIMessage) and last_message.tool_calls:
            return "tools"
        return END

    builder.add_conditional_edges("agent", should_continue, ["tools", END])
    builder.add_edge(
        "tools", "agent"
    )  # Return to agent after tool to possibly say something else

    graph = builder.compile()

    print("\n--- Graph Visualization (Mermaid) ---")
    try:
        print(graph.get_graph().draw_mermaid())
    except Exception as e:
        print(f"Could not draw mermaid graph: {e}")

    # --- Run Scenarios ---

    # Scenario 1: Git
    print("\n--- Scenario 1: Git Status ---")
    inputs = {"messages": [HumanMessage(content="Check git status")]}
    for chunk in graph.stream(inputs):
        for key, value in chunk.items():
            print(f"Node '{key}':")
            # print(value) # Verbose

    # Scenario 2: Spark
    print("\n--- Scenario 2: Spark SQL ---")
    inputs = {"messages": [HumanMessage(content="Query sales data")]}
    for chunk in graph.stream(inputs):
        for key, value in chunk.items():
            print(f"Node '{key}':")


if __name__ == "__main__":
    run_demo()
