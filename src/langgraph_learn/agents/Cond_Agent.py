from typing import TypedDict, NotRequired, Union, Optional
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    a: int
    b: int
    op: str
    res: NotRequired[Union[int, float]]

def add_node(state: AgentState) -> AgentState:
    "Addition Operator"
    state['res'] = state["a"] + state["b"]
    return state

def sub_node(state: AgentState) -> AgentState:
    "Subtraction Operator"
    state['res'] = state["a"] - state["b"]
    return state

def mul_node(state: AgentState) -> AgentState:
    "Multiply Operator"
    state['res'] = state["a"] * state["b"]
    return state

def div_node(state: AgentState) -> AgentState:
    "Divide Operator"
    state['res'] = state["a"] / state["b"]
    return state

def conditional_node(state: AgentState) -> Optional[str]:
    "Decides appropriate node for appropriate operator"

    if state["op"] == "+":
        return "add"
    elif state["op"] == "-":
        return "sub"
    elif state["op"] == "*":
        return "mul"
    elif state["op"] == "/":
        return "div"


graph = StateGraph(AgentState)

graph.add_node("Add", add_node)
graph.add_node("Subtract", sub_node)
graph.add_node("Multiply", mul_node)
graph.add_node("Divide", div_node)

graph.add_node("router", lambda state: state)

graph.add_edge(START, "router")
graph.add_conditional_edges("router", conditional_node, {
    # Edge: Node Mapping
    "add": "Add",
    "sub": "Subtract",
    "mul": "Multiply",
    "div": "Divide"
})

graph.add_edge("Add", END)
graph.add_edge("Subtract", END)
graph.add_edge("Multiply", END)
graph.add_edge("Divide", END)

app = graph.compile()
with open("graph.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())

result = app.invoke({
    "a": 2,
    "b": 3,
    "op": "+"
})
print(result)
