
import sys
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum
import logging
from typing import Optional
from uuid import UUID, uuid4
import uvicorn
from ..model import states, utils
from ..model import graph as graph_module


# Logging configuration
logger = logging.getLogger(__name__)


app = FastAPI()


class LanggraphConfig(BaseModel):
    thread_id : str = "4"
    iteraciones : int
    verbose :int


@app.get("/analisis/")
def get_analisis(cv : str, oferta : str):
    candidato = states.Candidato(id=utils.get_id(), cv=cv, oferta=oferta)
    graph_config = LanggraphConfig(thread_id="4",iteraciones=10,verbose=0)
    logger.info(f"Graph mode using FAST-API")
    logger.info("Creating graph and compiling workflow...")
    graph = graph_module.create_graph()
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

