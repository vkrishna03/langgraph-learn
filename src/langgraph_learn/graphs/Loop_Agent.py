from typing import TypedDict, NotRequired, List
from langgraph.graph import StateGraph, END
import random

class AgentState(TypedDict):
    name: str
    num: NotRequired[List[int]]
    counter: NotRequired[int]
    iteration_limit: int
    message: NotRequired[str]

def greeting_node(state: AgentState) -> AgentState:
    "Says Hi to the user."

    state['message'] = "Hi, " + f"{state['name']}!"
    state['counter'] = 0
    state["num"] = []
    return state

def random_node(state: AgentState) -> AgentState:
    "generates a random number from 0 to 10"

    if "num" in state:
        state['num'].append(random.randint(0,10))
    if "counter" in state:
        state['counter'] += 1

    return state

def should_continue(state: AgentState) -> str:
    "determines if we should continue generating or not"

    if "counter" in state and state['counter'] < state['iteration_limit']:
        print("entering loop no: ", state['counter'])
        return "loop"

    return "exit"

graph = StateGraph(AgentState)

graph.add_node("Greet", greeting_node)
graph.add_node("Random", random_node)

graph.add_edge("Greet", "Random")

graph.add_conditional_edges("Random", should_continue, {
    "loop": "Random",
    "exit": END
})

graph.set_entry_point("Greet")

app = graph.compile()
with open("graph.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())

result = app.invoke({
    "name": "kris",
    "iteration_limit": 5
})
print(result)
