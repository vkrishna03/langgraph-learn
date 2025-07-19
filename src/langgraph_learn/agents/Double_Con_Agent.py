from typing import TypedDict, NotRequired, Union, Optional
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    a: int
    b: int
    c: int
    op1: str
    op2: str
    res: NotRequired[Union[int, float]]
    message: NotRequired[str]

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
    if "res" in state:
        state['res'] = state["res"] * state["c"]
    return state

def div_node(state: AgentState) -> AgentState:
    "Divide Operator"
    if "res" in state:
        state['res'] = state["res"] / state["c"]
    return state

def err_node(state: AgentState) -> AgentState:
    "Error Node"
    state["message"] = "Unsupported operator!"
    return state

def first_conditional_node(state: AgentState) -> Optional[str]:
    "Decides appropriate node for appropriate operator"

    if state["op1"] == "+":
        return "add"
    elif state["op1"] == "-":
        return "sub"
    else:
        return "err"

def second_conditional_node(state: AgentState) -> Optional[str]:
    "Decides appropriate node for appropriate operator"

    if state["op2"] == "*":
        return "mul"
    elif state["op2"] == "/":
        return "div"
    else:
        return "err"


graph = StateGraph(AgentState)

# Adding Nodes - after router 1
graph.add_node("Add", add_node)
graph.add_node("Subtract", sub_node)

# Adding Nodes - after router 2
graph.add_node("Multiply", mul_node)
graph.add_node("Divide", div_node)

# Fallback node for error
graph.add_node("Error", err_node)

# router nodes
graph.add_node("router", lambda state: state)
graph.add_node("router2", lambda state: state)

# router to add, subtract
graph.add_edge(START, "router")
graph.add_conditional_edges("router", first_conditional_node, {
    # Edge: Node Mapping
    "add": "Add",
    "sub": "Subtract",
    "err": "Error"
})

# add, subtract to router 2, err to end
graph.add_edge("Add", "router2")
graph.add_edge("Subtract", "router2")
graph.add_edge("Error", END)

# router to mul, div
graph.add_conditional_edges("router2", second_conditional_node, {
    # Edge: Node Mapping
    "mul": "Multiply",
    "div": "Divide",
    "err": "Error"
})

# mul, div to end
graph.add_edge("Multiply", END)
graph.add_edge("Divide", END)

app = graph.compile()
with open("graph.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())

result = app.invoke({
    "a": 2,
    "b": 3,
    "c": 8,
    "op1": "+",
    "op2": "*"
})
print(result)
