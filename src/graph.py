import logging
import logging.config
import logging.handlers
from langchain_core.runnables import RunnableLambda
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
from langchain_core.messages import HumanMessage
from .models import get_open_ai_json
from .states import (
    State,
    Candidato,
    Analisis
)
from .agents import (
    analyzer_agent,
    reviewer_agent,
    final_report,
    end_node
)

logger = logging.getLogger(__name__)

def create_graph(candidato):
    
    graph = StateGraph(State)
    graph.add_node("analyzer",lambda state: analyzer_agent(state=state))
    graph.add_node( "reviewer", lambda state: reviewer_agent(state=state))
    graph.add_node( "report", lambda state: final_report(state=state))
    graph.add_node( "end", lambda state: end_node(state=state))

    # Define the edges in the agent graph
    def pass_review(state: State):
        alucinacion = state["alucinacion"]
        
        if alucinacion == 1 or alucinacion == 1.0:
            next_agent = "analyzer"
        else:
            next_agent = "end"
            
        return next_agent

    # Add edges to the graph
    graph.set_entry_point("analyzer")
    graph.set_finish_point("end")
    graph.add_edge("analyzer", "reviewer")
    graph.add_conditional_edges( "reviewer",lambda state: pass_review(state=state),)
    graph.add_edge("final_report", "end")

    return graph

def compile_workflow(graph):
    # memory = SqliteSaver.from_conn_string(":memory:")  # Here we only save in-memory
    # workflow = graph.compile(checkpointer=memory, interrupt_before=["end"])
    workflow = graph.compile()
    return workflow