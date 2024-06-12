import yaml
import os
import logging
from termcolor import colored
from typing import Dict, List, Tuple, Union, Optional, Callable
from pydantic import BaseModel, ValidationError
from .states import (
    State,
    Analisis,
    Candidato
)
from .models import get_open_ai_json
from .chains import (
    get_reviewer_chain,
    get_analyzer_chain
)

from .utils import get_id,get_current_spanish_date_iso

# Logging configuration
logger = logging.getLogger(__name__)

def analyzer_agent(state:State, get_chain : Callable = get_analyzer_chain):
    
    logger.info(f"Estado previo [Analyzer-Agent] : \n {state}")
    
    analyzer_chain = get_chain()

    candidato = state["candidato"]
    logger.info(f"Análisis del candidato : \n {candidato}")
    
    raw_response = analyzer_chain.invoke(input={"cv": candidato.cv, "oferta": candidato.oferta})
    logger.info(f"Análisis del modelo : \n {raw_response}")
    print(colored(f"Analyzer-Agent 👩🏿‍💻: {raw_response}", 'cyan'))
    
    # Manejo de una respuesta del modelo en un formato no correcto [no alineado con pydantic BaseModel]
    try:
        analisis = Analisis(**raw_response,id=candidato.id , status="OK")  # Instancia de Pydantic Analisis BaseModel object
    except ValidationError as e:
        logger.exception(f'{e} : Formato de respuesta del modelo incorrecta')
        analisis = Analisis(puntuacion=0, experiencias=list(),id=candidato.id, descripcion="", status="ERROR")
        
        
    if state["analisis"]:
        state["analisis"].append(analisis)
    else:
        state["analisis"] = [analisis]
    logger.info(f"Estado tras Analyzer-Agent : \n {state}")

    return state

def reviewer_agent(state:State, get_chain : Callable = get_reviewer_chain):
    
    logger.info(f"Estado previo [Reviewer-Agent] : \n {state}")
    
    reviewer_chain = get_chain()

    candidato = state["candidato"]
    analisis_previo = state["analisis"][-1]
    logger.info(f"Revision del candidato : \n {candidato}")
    logger.info(f"Analisis previo : \n {analisis_previo}")
    
    alucinacion = reviewer_chain.invoke(input={"cv": candidato.cv, "oferta": candidato.oferta, "analisis":analisis_previo})
    logger.info(f"Revision del modelo : \n {alucinacion}")
    print(colored(f"Reviewer-Agent 👩🏽‍⚖️: {alucinacion}", 'magenta'))
    
    # Manejo de una respuesta del modelo en un formato no correcto [no alineado con tipo Union[int,float] de clave "alucinacion"]
    if not isinstance(alucinacion["alucinacion"], (int,float)):
        raise ValueError(f"El  Reviewer-Agent esta devolviendo una alucionacion : {alucinacion} no alineada con tipo de dato Union[int,float]")
    
    state = {**state, "alucinacion": alucinacion["alucinacion"]}
    logger.info(f"Estado tras Reviewer-Agent : \n {state}")

    return state


def final_report(state:State):

    analisis_final = state["analisis"][-1]
    
    logger.info(f"Analisis final : \n {analisis_final}")
    print(colored(f"Final Report 📝: {analisis_final}", 'blue'))

    state = {**state, "analisis_final": analisis_final}

    return state

def end_node(state:State):
    logger.info(f"Nodo final")
    state = {**state, "end_chain": True}
    return state