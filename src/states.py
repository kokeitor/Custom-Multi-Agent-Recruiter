from typing import Dict, List, Tuple, Union, Optional, Callable, ClassVar, TypedDict, Annotated
from pydantic import BaseModel
from langgraph.graph.message import add_messages

class Analisis(BaseModel):
    id : str
    puntuacion: int
    experiencias: List[Dict[str,str]]
    descripcion: str
    status: str
    
class Candidato(BaseModel):
    id : str
    cv : str
    oferta : str

class State(TypedDict):
    candidato : Candidato
    analisis : List[Analisis]
    alucinacion : Union[int,float] 
    analisis_final : str
    final : bool