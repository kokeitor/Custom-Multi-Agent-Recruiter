from typing import Dict, List, Tuple, Union, Optional, Callable, ClassVar, TypedDict, Annotated
from pydantic import BaseModel
from langchain.prompts import PromptTemplate
from dataclasses import dataclass


class Analisis(BaseModel):
    id : str
    candidato_id : str
    fecha : str
    puntuacion: int
    experiencias: List[Dict[str,str]]
    descripcion: str
    status: str
    
class Candidato(BaseModel):
    id : Optional[str] = None
    cv : str
    oferta : str

class State(TypedDict):
    candidato : Candidato
    analisis : List[Analisis]
    alucinacion_cv : Union[int,float,str] 
    alucinacion_oferta : Union[int,float,str] 
    analisis_final : Analisis
    
@dataclass()  
class Agent:
    agent_name : str
    model : str
    get_model : Callable
    temperature : float
    prompt : PromptTemplate
    