from typing import TypedDict, List, Optional, NotRequired
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    values: List[int]
    operator: str
    result: NotRequired[int]
    message: NotRequired[str]

def math_node(state: AgentState) -> AgentState:
    "Performs math operations!"
    if state["operator"] == "+":
        state["result"] = 0
        for val in state["values"]:
            state["result"] += val

        state["message"] = "Operation performed successfully!"
        return state
    elif state["operator"] == "*":
        state["result"] = 1
        for val in state["values"]:
            state["result"] *= val

        state["message"] = "Operation performed successfully!"
        return state
    else:
        state["message"] = "Unknown error!"
        return state

graph = StateGraph(AgentState)

graph.add_node("Math", math_node)

graph.set_entry_point("Math")
graph.set_finish_point("Math")

app = graph.compile()

with open("graph.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())

result = app.invoke({
    "values": [1,2,3,4,5],
    "operator": "*"
})
print(result)
