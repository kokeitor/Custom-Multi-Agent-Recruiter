
import sys
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
import uvicorn
from model import states, utils
from model import graph as graph_module
from model.modes import ConfigGraphApi


# Logging configuration
logger = logging.getLogger(__name__)

app = FastAPI()


@app.put("/analisis/")
def get_analisis(cv : str, oferta : str):
    
    candidato = states.Candidato(id=utils.get_id(), cv=cv, oferta=oferta)
    logger.info(f"{candidato=}")
    
    CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'generation.json')
    logger.info(f"{CONFIG_PATH=}")
    graph_config = ConfigGraphApi(config_path=CONFIG_PATH)
    
    logger.info(f"Graph mode using FAST-API")
    logger.info("Creating graph and compiling workflow...")
    graph = graph_module.create_graph(config=graph_config)
    compiled_graph = graph_module.compile_graph(graph)
    logger.info("Graph and workflow created")
    
    try:
        response = compiled_graph.invoke(  
                                    input={"candidato": candidato}, 
                                    config=graph_config.runnable_config,
                                    stream_mode='values'
                                )
    except Exception as e:
        print(f"{e}")
        response = False
        
    if response:
        if response["analisis_final"]:
            analisis =  response["analisis_final"]
        else:
            analisis = "ERROR RESPONSE"
    else:
        analisis = "ERROR GRAPH"
        
    return {"Analysis" : analisis}

def run_fast_api() -> None:
    uvicorn.run(app, host = "0.0.0.0", port =8050)

