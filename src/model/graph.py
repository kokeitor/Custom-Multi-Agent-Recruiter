import logging
import logging.config
import logging.handlers
from langchain_core.runnables import RunnableLambda
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
from langchain_core.messages import HumanMessage
from .modes import ConfigGraph
from .states import (
    State,
    Candidato,
    Analisis
)
from .agents import (
    analyzer_agent,
    reviewer_cv_agent,
    reviewer_offer_agent,
    final_report,
    end_node,
)

logger = logging.getLogger(__name__)

def create_graph(config : ConfigGraph):
    
    analyzer = config.agents.get("analyzer",None)
    re_analyzer = config.agents.get("re_analyzer",None)
    cv_reviewer = config.agents.get("cv_reviewer",None)
    offer_reviewer = config.agents.get("offer_reviewer",None)

    graph = StateGraph(State)
    graph.add_node("analyzer",lambda state: analyzer_agent(state=state,analyzer=analyzer, re_analyzer=re_analyzer))
    graph.add_node("reviewer_cv",lambda state: reviewer_cv_agent(state=state, agent=cv_reviewer))
    graph.add_node( "reviewer_offer", lambda state: reviewer_offer_agent(state=state, agent=offer_reviewer))
    graph.add_node( "report", lambda state: final_report(state=state))
    graph.add_node( "end_node", lambda state: end_node(state=state))

    # Define the edges in the agent graph
    def pass_offer_review(state: State):
        alucinacion = state["alucinacion_oferta"]
        
        if alucinacion == 1 or alucinacion == 1.0:
            next_agent = "analyzer"
        else:
            next_agent = "report"
            
        return next_agent
    
    # Define the edges in the agent graph
    def pass_cv_review(state: State):
        alucinacion_cv = state["alucinacion_cv"]
        
        if alucinacion_cv == 1 or alucinacion_cv == 1.0:
            next_agent = "analyzer"
        else:
            next_agent = "reviewer_offer"
            
        return next_agent

    # Add edges to the graph
    graph.set_entry_point("analyzer")
    graph.set_finish_point("end_node")
    graph.add_edge("analyzer", "reviewer_cv")
    graph.add_conditional_edges( "reviewer_cv",lambda state: pass_cv_review(state=state),)
    graph.add_conditional_edges( "reviewer_offer",lambda state: pass_offer_review(state=state))
    graph.add_edge("report","end_node")

    return graph

def compile_workflow(graph):
    workflow = graph.compile()
    return workflow