from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from dotenv import load_dotenv
import os

load_dotenv()

class AgentState(TypedDict):
    messages: List[Dict[str, Any]]
    current_agent: str
    task: str
    research_data: Dict[str, Any]
    final_response: str
    needs_research: bool
    needs_planning: bool

# Initialize tools and LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
search_tool = DuckDuckGoSearchRun()
wikipedia = WikipediaAPIWrapper()

def search_agent(state: AgentState) -> AgentState:
    """Agent responsible for web search"""
    query = state["task"]
    print(f"🔍 Search Agent: Searching for '{query}'")

    try:
        search_results = search_tool.run(query)
        state["research_data"]["search_results"] = search_results
        state["messages"].append({
            "role": "assistant",
            "content": f"Found search results for '{query}': {search_results[:500]}..."
        })
    except Exception as e:
        state["messages"].append({
            "role": "assistant",
            "content": f"Search failed: {str(e)}"
        })

    return state

def wikipedia_agent(state: AgentState) -> AgentState:
    """Agent responsible for Wikipedia research"""
    query = state["task"]
    print(f"📚 Wikipedia Agent: Researching '{query}'")

    try:
        wiki_results = wikipedia.run(query)
        state["research_data"]["wikipedia_info"] = wiki_results
        state["messages"].append({
            "role": "assistant",
            "content": f"Wikipedia research on '{query}': {wiki_results[:500]}..."
        })
    except Exception as e:
        state["messages"].append({
            "role": "assistant",
            "content": f"Wikipedia research failed: {str(e)}"
        })

    return state

def planner_agent(state: AgentState) -> AgentState:
    """Agent that plans and coordinates tasks"""
    task = state["task"]
    print(f"📋 Planner Agent: Analyzing task '{task}'")

    # Determine what research is needed
    prompt = f"""Analyze this task and determine what research is needed: {task}

    Return a JSON-like response indicating:
    - needs_research: true/false
    - needs_wikipedia: true/false
    - needs_search: true/false
    - complexity: "simple"/"medium"/"complex"
    """

    response = llm.invoke([HumanMessage(content=prompt)])
    analysis = response.content.lower()

    state["needs_research"] = "needs_research" in analysis or "research" in task.lower()
    state["research_data"]["analysis"] = analysis

    state["messages"].append({
        "role": "assistant",
        "content": f"Task analysis: {analysis}"
    })

    return state

def synthesizer_agent(state: AgentState) -> AgentState:
    """Agent that synthesizes all information into final response"""
    print("🧠 Synthesizer Agent: Creating final response")

    all_info = []
    all_info.append(f"Original Task: {state['task']}")

    if state["research_data"].get("search_results"):
        all_info.append(f"Search Results: {state['research_data']['search_results'][:1000]}")

    if state["research_data"].get("wikipedia_info"):
        all_info.append(f"Wikipedia Info: {state['research_data']['wikipedia_info'][:1000]}")

    if state["research_data"].get("analysis"):
        all_info.append(f"Analysis: {state['research_data']['analysis']}")

    synthesis_prompt = f"""Based on the following information, provide a comprehensive response to the task:

    {' '.join(all_info)}

    Provide a clear, helpful response."""

    final_response = llm.invoke([HumanMessage(content=synthesis_prompt)])

    state["final_response"] = final_response.content
    state["messages"].append({
        "role": "assistant",
        "content": f"Final Answer: {final_response.content}"
    })

    return state

def router_agent(state: AgentState) -> str:
    """Routes to appropriate next agent based on current state"""
    if not state.get("research_data"):
        state["research_data"] = {}

    # First, always go to planner
    if state["current_agent"] == "start":
        return "planner"

    # After planning, decide research path
    if state["current_agent"] == "planner":
        if state.get("needs_research", False):
            return "search"
        else:
            return "synthesizer"

    # After search, go to wikipedia if needed
    if state["current_agent"] == "search":
        if "wikipedia" in state.get("research_data", {}).get("analysis", "").lower():
            return "wikipedia"
        else:
            return "synthesizer"

    # After wikipedia, synthesize
    if state["current_agent"] == "wikipedia":
        return "synthesizer"

    return "synthesizer"

# Create the graph
graph = StateGraph(AgentState)

# Add nodes
graph.add_node("planner", planner_agent)
graph.add_node("search", search_agent)
graph.add_node("wikipedia", wikipedia_agent)
graph.add_node("synthesizer", synthesizer_agent)

# Add edges
graph.add_edge(START, "planner")

# Conditional edges based on router
graph.add_conditional_edges(
    "planner",
    router_agent,
    {
        "search": "search",
        "synthesizer": "synthesizer"
    }
)

graph.add_conditional_edges(
    "search",
    router_agent,
    {
        "wikipedia": "wikipedia",
        "synthesizer": "synthesizer"
    }
)

graph.add_conditional_edges(
    "wikipedia",
    router_agent,
    {
        "synthesizer": "synthesizer"
    }
)

graph.add_edge("synthesizer", END)

# Compile the graph
agent_app = graph.compile()

def run_agentic_ai(task: str) -> Dict[str, Any]:
    """Run the complete agentic AI system"""
    initial_state = {
        "messages": [{"role": "user", "content": task}],
        "current_agent": "start",
        "task": task,
        "research_data": {},
        "final_response": "",
        "needs_research": False,
        "needs_planning": True
    }

    result = agent_app.invoke(initial_state)
    return result

if __name__ == "__main__":
    # Test the system
    test_task = "What are the benefits of renewable energy?"
    result = run_agentic_ai(test_task)
    print("Final Response:", result["final_response"])