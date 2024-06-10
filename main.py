import os
import json
import logging
import logging.config
import logging.handlers
from dotenv import load_dotenv
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser,StrOutputParser
from langchain_community.chat_models import ChatOllama
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_openai import ChatOpenAI
from dataclasses import dataclass
from typing import Dict, List, Tuple, Union, Optional, Callable, ClassVar
from langchain.chains.llm import LLMChain
from pydantic import BaseModel
from src.module import prompts
from src.module import models
from src.module import chains
from src.module.utils import (
                get_current_spanish_date_iso,
                setup_logging
)
import warnings


# Load environment variables from .env file
load_dotenv()


# Set environment variables
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['PINECONE_API_KEY'] = os.getenv('PINECONE_API_KEY')
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ['LLAMA_CLOUD_API_KEY'] = os.getenv('LLAMA_CLOUD_API_KEY')
os.environ['HF_TOKEN'] = os.getenv('HUG_API_KEY')


# Logging configuration
logger = logging.getLogger("Main")


class Analisis(BaseModel):
    respuesta : str


@dataclass()
class CvAnalyzer:
    chain : LLMChain
    cv : str
    oferta : str
    
    def invoke(self,input_chain: dict):
        return self.chain.invoke(input_chain)
    
    
@dataclass()
class Pipeline:
    config_path : Optional[str] = None
    config : Optional[dict] = None
    
    def __post_init__(self):
        if self.config is None and self.config_path is not None:
            self.config = self.get_config()
        if self.config is not None and self.config_path is not None:
            logger.warning("Definidas dos configuraciones [archivho json y dict] -> da prioridad a dict config")
        if self.config is None and self.config_path is None:
            logger.exception("No se ha proporcionado ninguna configuracion para la generacion")
            raise AttributeError("No se ha proporcionado ninguna configuracion para la generacion")
        
        self.chain = chains.classify_chain # Objeto base chain para la tarea de analisis de Cvs
        self.cv = self.config.get("cv",None)
        self.oferta = self.config.get("oferta",None)
        if self.cv is not None and self.oferta is not None:
            self.analyzer_chain = self.get_analyzer() # Objeto base chain 'customizado' para tarea analisis de Cvs [incluye atrb el cv y oferta especifico]
            logger.info(f"Cv -> {self.cv}")
            logger.info(f"Oferta de Empleo -> {self.oferta}")
        else:
            logger.exception("No se ha proporcionado ningun Cv ni oferta de empleo para el analisis")
            raise ValueError("No se ha proporcionado ningun Cv ni oferta de empleo para el analisis")
        
    def get_config(self) -> dict:
        if not os.path.exists(self.config_path):
            logger.exception(f"Archivo de configuracion no encontrado en {self.config_path}")
            raise FileNotFoundError(f"Archivo de configuracion no encontrado en {self.config_path}")
        with open(self.config_path, encoding='utf-8') as file:
            config = json.load(file)
        return config
        
    def get_analyzer(self) -> CvAnalyzer:
        return CvAnalyzer(chain=self.chain, cv=self.cv, oferta=self.oferta)

    def run(self) -> Analisis:
        """Run Pipeline -> Invoca langchain chain -> genera objeto Analisis con respuesta del modelo"""
        self.analisis = Analisis(respuesta=dict(self.analyzer_chain.invoke(input_chain={"cv": self.cv, "oferta": self.oferta})))
        logger.info(f"Analisis del modelo : {self.analisis}")
        return self.analisis
        

def main() -> None:
    CONFIG = "./config/generate.json"
    setup_logging()
    pipeline = Pipeline(config_path=CONFIG)
    analysis = pipeline.run()
    
if __name__ == '__main__':
    main()