from typing import TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    message: str

def hello_world_node(state: AgentState) -> AgentState:
    "Node that says Hello World!"
    state["message"] = "Hello " + state["message"] + "!";
    return state;

graph = StateGraph(AgentState)

graph.add_node("Hello World",hello_world_node)

graph.set_entry_point("Hello World")
graph.set_finish_point("Hello World")

app = graph.compile()

with open("graph.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())

result = app.invoke({"message": "Krishna"})
print(result)
