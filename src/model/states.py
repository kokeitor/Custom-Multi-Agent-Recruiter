from typing import Dict, List, Tuple, Union, Optional, Callable, ClassVar, TypedDict, Annotated
from pydantic import BaseModel
from langchain.prompts import PromptTemplate

from langgraph.graph.message import add_messages

class Analisis(BaseModel):
    id : str
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
    alucinacion_cv : Union[int,float] 
    alucinacion_oferta : Union[int,float] 
    analisis_final : Analisis
    
class Agent(BaseModel):
    agent_name : str
    model_name : str
    model : Callable
    temperature : float
    prompt : PromptTemplate
