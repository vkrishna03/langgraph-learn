from typing import TypedDict, NotRequired, List, Optional
from langgraph.graph import StateGraph, END
import random

class AgentState(TypedDict):
    name: str
    guesses: NotRequired[List[int]]
    attempts_count: NotRequired[int]
    lower_bound: int
    higher_bound: int
    hint: NotRequired[str]
    num: int

MAX_LIMIT: int = 7

def setup_node(state: AgentState) -> AgentState:
    "sets up the game"
    state['guesses'] = []
    state['attempts_count'] = 0
    return state

def guess_node(state: AgentState) -> AgentState:
    "guesses numbers based on hint"

    if "attempts_count" in state:
        state["attempts_count"] += 1

    if 'guesses' in state:
        if 'hint' in state:
            if state["hint"] == "higher":
                state["lower_bound"] = state["guesses"][-1] + 1
            elif state["hint"] == "lower":
                state["higher_bound"] = state["guesses"][-1] - 1

        state['guesses'].append(random.randint(state['lower_bound'], state['higher_bound']))
    return state

def hint_node(state: AgentState) -> AgentState:
    "Gives if the guessed number is higher or lower"
    if "guesses" in state:
        if state["guesses"][-1] > state["num"]:
            state["hint"] = "lower"
        elif state["guesses"][-1] < state["num"]:
            state["hint"] = "higher"

    return state

def should_continue(state: AgentState) -> str:
    "determines if to continue or not"
    if "attempts_count" in state and state["attempts_count"] < MAX_LIMIT:
        if "guesses" in state and state["guesses"][-1] == state["num"]:
            return "exit"
        else:
            return "continue"
    else:
        return "exit"


graph = StateGraph(AgentState)

graph.add_node("Setup", setup_node)
graph.add_node("Guess", guess_node)
graph.add_node("Hint", hint_node)

graph.add_edge("Setup", "Guess")
graph.add_edge("Guess", "Hint")

graph.add_conditional_edges("Hint", should_continue,{
    "continue": "Guess",
    "exit": END
})

graph.set_entry_point("Setup")

app = graph.compile()
with open("graph.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())

results = app.invoke({
    "name": "Krishna",
    "num": 7,
    "lower_bound": 0,
    "higher_bound": 100
})
print(results)
