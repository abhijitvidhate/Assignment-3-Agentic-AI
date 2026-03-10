#!/usr/bin/env python3
"""
Agentic AI System Demo - Shows the graph structure and workflow
"""

from agentic_ai_system import graph
from IPython.display import Image, display
import matplotlib.pyplot as plt
import networkx as nx

def visualize_graph():
    """Visualize the agent workflow graph"""
    print("🤖 Agentic AI System - Graph Visualization")
    print("=" * 50)

    # Get the Mermaid diagram
    try:
        mermaid_png = graph.get_graph().draw_mermaid_png()
        print("✅ Graph compiled successfully!")

        # Try to display the image (works in Jupyter)
        try:
            display(Image(mermaid_png))
        except:
            print("📊 Graph visualization generated (display in Jupyter notebook)")

    except Exception as e:
        print(f"❌ Graph visualization error: {e}")

    # Show the node structure
    print("\n🏗️  Agent Architecture:")
    print("1. 📋 Planner Agent - Analyzes tasks and plans research")
    print("2. 🔍 Search Agent - Performs web searches")
    print("3. 📚 Wikipedia Agent - Gathers detailed information")
    print("4. 🧠 Synthesizer Agent - Combines all information")

    print("\n🔀 Workflow:")
    print("User Query → Planner → [Search → Wikipedia] → Synthesizer → Final Response")

    print("\n✨ Key Features:")
    print("- Intelligent routing based on task complexity")
    print("- Multi-source research integration")
    print("- Coordinated agent collaboration")
    print("- Production-ready FastAPI backend")

def demo_workflow():
    """Show example workflow without API calls"""
    print("\n🎯 Example Workflow:")
    print("Task: 'What are the benefits of renewable energy?'")

    print("\n📋 Step 1 - Planner Agent:")
    print("   Analysis: 'This requires research on renewable energy benefits'")
    print("   Decision: needs_research=True, needs_search=True, needs_wikipedia=True")

    print("\n🔍 Step 2 - Search Agent:")
    print("   Query: 'benefits of renewable energy'")
    print("   Result: Web search results from DuckDuckGo")

    print("\n📚 Step 3 - Wikipedia Agent:")
    print("   Query: 'renewable energy'")
    print("   Result: Detailed information from Wikipedia")

    print("\n🧠 Step 4 - Synthesizer Agent:")
    print("   Combines: Search results + Wikipedia info + Analysis")
    print("   Output: Comprehensive final answer")

if __name__ == "__main__":
    visualize_graph()
    demo_workflow()

    print("\n🚀 Ready for deployment!")
    print("Run: ./run_local.sh (after adding OpenAI API key to .env)")
    print("Or: docker-compose up -d")