from langgraph.graph import StateGraph, START, END
from state import *
from nodes import *

# initializing state graph
graph = StateGraph(AgentState)

# Adding node to the graph
graph.add_node("security", security_node)
graph.add_node("style", style_node)
graph.add_node("complexity", complexity_node)
graph.add_node("best_practices", best_practices_node)
graph.add_node("test_coverage", test_coverage_node)
graph.add_node("performance", performance_node)
graph.add_node("dependency", dependency_node)
graph.add_node("documentation", documentation_node)
graph.add_node("accessibility", accessibility_node)
graph.add_node("synthesis", synthesis_node)

# Connecting sequentially
graph.add_edge(START, "security")
graph.add_edge("security", "style")
graph.add_edge("style", "complexity")
graph.add_edge("complexity", "best_practices")
graph.add_edge("best_practices", "test_coverage")
graph.add_edge("test_coverage", "performance")
graph.add_edge("performance", "dependency")
graph.add_edge("dependency", "documentation")
graph.add_edge("documentation", "accessibility")
graph.add_edge("accessibility", "synthesis")
graph.add_edge("synthesis", END)

graph_app = graph.compile()


