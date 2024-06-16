
import sys
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
import uvicorn
from ..model import states, utils
from ..model import graph as graph_module
from ..model.modes import ConfigGraphApi


# Logging configuration
logger = logging.getLogger(__name__)

app = FastAPI()

class LangGraphConfig(BaseModel):
    thread_id : str = "4"
    iteraciones : int
    verbose :int

@app.get("/analisis/")
def get_analisis(cv : str, oferta : str):
    
    candidato = states.Candidato(id=utils.get_id(), cv=cv, oferta=oferta)
    graph_config = LangGraphConfig(thread_id="4",iteraciones=10,verbose=0)
    CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'generation.json')
    logger.info(f"{CONFIG_PATH=}")
    agent_config = ConfigGraphApi(config_path=CONFIG_PATH)
    logger.info(f"Graph mode using FAST-API")
    logger.debug(f"{candidato=}")
    logger.debug(f"{graph_config=}")
    logger.info("Creating graph and compiling workflow...")
    graph = graph_module.create_graph(config=agent_config)
    workflow = graph_module.compile_workflow(graph)
    logger.info("Graph and workflow created")
    
    thread = {"configurable": {"thread_id": graph_config.thread_id}}
    iteraciones = {"recursion_limit":graph_config.iteraciones }
    
    input_candidato = {"candidato": candidato}
    logger.info(f"Start analisis for {candidato=}")
    logger.debug(f"Cv Candidato -> {candidato.cv}")
    logger.debug(f"Oferta de Empleo para candidato-> {candidato.oferta}")
    
    estados = [event for event in workflow.stream(input_candidato, iteraciones)]
    return {"Final graph state" : estados[-1]}

def run_fast_api() -> None:
    uvicorn.run(app, host = "0.0.0.0", port =8000)

