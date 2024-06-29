import os
import logging
import logging.config
import logging.handlers
from langgraph.graph import StateGraph, END
from langgraph.checkpoint import MemorySaver
from langgraph.graph.graph import CompiledGraph
from langchain_core.runnables.graph import MermaidDrawMethod
from modes import ConfigGraph
from states import State
from agents import (
    analyzer_agent,
    reviewer_cv_agent,
    reviewer_offer_agent,
    final_report
    )
from utils import get_current_spanish_date_iso_file_name_format


logger = logging.getLogger(__name__)


def create_graph(config : ConfigGraph) -> StateGraph:
    
    analyzer = config.agents.get("analyzer",None)
    re_analyzer = config.agents.get("re_analyzer",None)
    cv_reviewer = config.agents.get("cv_reviewer",None)
    offer_reviewer = config.agents.get("offer_reviewer",None)

    graph = StateGraph(State)
    graph.add_node("analyzer",lambda state: analyzer_agent(state=state,analyzer=analyzer, re_analyzer=re_analyzer))
    graph.add_node("reviewer_cv",lambda state: reviewer_cv_agent(state=state, agent=cv_reviewer))
    graph.add_node( "reviewer_offer", lambda state: reviewer_offer_agent(state=state, agent=offer_reviewer))
    graph.add_node( "report", lambda state: final_report(state=state))
  
    # Define the edges in the agent graph
    def route_offer_review(state: State):
        alucinacion = state["alucinacion_oferta"]
        
        if alucinacion == 1 or alucinacion == 1.0:
            next_agent = "analyzer"
        else:
            next_agent = "report"
            
        return next_agent
    
    # Define the edges in the agent graph
    def route_cv_review(state: State):
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
    graph.add_conditional_edges(
                                source="reviewer_cv",
                                path=route_cv_review,
                                path_map={
                                    "analyzer":"analyzer",
                                    "reviewer_offer":"reviewer_offer",
                                }
                                )
    graph.add_conditional_edges(
                                source="reviewer_offer",
                                path=route_offer_review,
                                path_map={
                                    "analyzer":"analyzer",
                                    "report":"report",
                                }
                                )
    graph.add_edge("report",END)

    return graph


def compile_workflow(graph : StateGraph) -> CompiledGraph:
    workflow = graph.compile()
    return workflow


def save_graph(compile_graph : CompiledGraph) -> None:
    """Save graph as png in the default figure graph directory"""
    
    figure_path = os.path.join(os.path.dirname(__file__), "..", "data", "figures", "graphs", f'{get_current_spanish_date_iso_file_name_format()}_graph.png') 
    
    logger.debug(f"Attempting to save compiled graph -> {figure_path}")
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(figure_path), exist_ok=True)
    
    # Try saving the file
    try:
        with open(figure_path, 'wb') as f:
            f.write(get_png_graph(compile_graph=compile_graph))
    except Exception as e:
        logger.error(f"File cannot be saved : {figure_path} -> {e}")
        
    # Debugging: Check if file is created
    if os.path.exists(figure_path):
        logger.info(f"Compiled graph png succesfully saved -> {figure_path}")
    else:
        logger.error(f"Failed to save the compile graph png-> {figure_path}")
    

def get_png_graph(compile_graph : CompiledGraph) -> bytes:
    return compile_graph.get_graph().draw_mermaid_png(draw_method=MermaidDrawMethod.API)