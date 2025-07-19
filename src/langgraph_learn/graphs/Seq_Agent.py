from typing import TypedDict, NotRequired
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    name: str
    age: int
    message: NotRequired[str]

def hello_node(state: AgentState) -> AgentState:
    state["message"] = "Hi " + state["name"] + "!"
    return state

def age_node(state: AgentState) -> AgentState:
    if "message" in state:
        state["message"] += f" You are {state['age']} years old!"
    return state

graph = StateGraph(AgentState)

graph.add_node("Hello", hello_node)
graph.add_node("Age", age_node)

graph.add_edge("Hello", "Age")

graph.set_entry_point("Hello")
graph.set_finish_point("Age")

app = graph.compile()
with open("graph.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())

# requires pygraphviz dependency
# app.get_graph().draw_png(output_file_path="graph-new.png")

result = app.invoke({
    "name": "kris",
    "age": 21
})
print(result)
