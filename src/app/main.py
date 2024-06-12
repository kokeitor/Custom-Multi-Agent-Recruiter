import os
import json
import logging
from termcolor import colored
from dotenv import load_dotenv
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dataclasses import dataclass
from typing import Dict, List, Tuple, Union, Optional, Callable, ClassVar
from langchain.chains.llm import LLMChain
from pydantic import BaseModel, ValidationError
from chains.chains import get_chain
from states.states import (
    Analisis,
    Candidato,
    State
)
from utils.utils import (
                        get_current_spanish_date_iso, 
                        setup_logging,
                        get_id,
                        get_arg_parser
                        )
from exceptions.exceptions import NoOpenAIToken

# Load environment variables from .env file
load_dotenv()

# Set environment variables
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
#os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ['LLAMA_CLOUD_API_KEY'] = os.getenv('LLAMA_CLOUD_API_KEY')
os.environ['HF_TOKEN'] = os.getenv('HUG_API_KEY')

# Logging configuration
logger = logging.getLogger("Main")

@dataclass()
class CvAnalyzer:
    chain: LLMChain
    def invoke(self, candidato: Candidato) -> dict:
        return self.chain.invoke(input={"cv": candidato.cv, "oferta": candidato.oferta})
    
@dataclass()
class Pipeline:
    config_path: Optional[str] = None
    config: Optional[dict] = None
    
    def __post_init__(self):
        if self.config is not None and self.config_path is not None:
            logger.warning("Definidas dos configuraciones [archivo json y dict] -> da prioridad a dict config")
        if self.config is None and self.config_path is not None:
            self.config = self.get_config()
            logger.info(f"Definida configuracion mediante archivo JSON en {self.config_path}")
        if self.config is None and self.config_path is None:
            logger.exception("No se ha proporcionado ninguna configuración para la generación")
            raise AttributeError("No se ha proporcionado ninguna configuración para la generación")
        
        self.chain = get_chain()  # Get objeto base chain para la tarea de análisis de CVs
        self.cv = self.config.get("cv", None)
        self.oferta = self.config.get("oferta", None)
        if self.cv is not None and self.oferta is not None:
            self.candidato = self.get_candidato() # Get obj Candidato
            self.analyzer_chain = self.get_analyzer()  # Get objeto base chain 'customizado' para tarea análisis de CVs [incluye atrb el cv y oferta específico]
            logger.debug(f"Cv Candidato -> {self.candidato.cv}")
            logger.debug(f"Oferta de Empleo para candidato-> {self.candidato.oferta}")
        else:
            logger.exception("No se ha proporcionado ningún CV ni oferta de empleo para el análisis")
            raise ValueError("No se ha proporcionado ningún CV ni oferta de empleo para el análisis")
        
    def get_config(self) -> dict:
        if not os.path.exists(self.config_path):
            logger.exception(f"Archivo de configuración no encontrado en {self.config_path}")
            raise FileNotFoundError(f"Archivo de configuración no encontrado en {self.config_path}")
        with open(self.config_path, encoding='utf-8') as file:
            config = json.load(file)
        return config
        
    def get_analyzer(self) -> CvAnalyzer:
        return CvAnalyzer(chain=self.chain)
    
    def get_candidato(self) -> Candidato:
        return Candidato(id=get_id(), cv=self.cv, oferta=self.oferta)

    def get_analisis(self) -> Analisis:
        """Run Pipeline -> Invoca langchain chain -> genera objeto Analisis con respuesta del modelo"""
        logger.info(f"Análisis del candidato : \n {self.candidato}")
        self._raw_response = self.analyzer_chain.invoke(candidato=self.candidato)  # Invoca a la chain que parsea la respuesta del modelo a python dict
        logger.info(f"Análisis del modelo : \n {self._raw_response}")
    
        # Manejo de una respuesta del modelo en un formato no correcto [no alineado con pydantic BaseModel]
        try:
            self.analisis = Analisis(**self._raw_response,id=self.candidato.id , status="OK")  # Instancia de Pydantic Analisis BaseModel object
            return self.analisis
        except ValidationError as e:
            logger.exception(f'{e} : Formato de respuesta del modelo incorrecta')
            return Analisis(puntuacion=0, experiencias=list(),id=self.candidato.id, descripcion="", status="ERROR")
        
def main() -> None:
    setup_logging() 
    parser = get_arg_parser()
    args = parser.parse_args()
    CONFIG_PATH = args.config_path
    OPENAI_API_KEY = args.token
    if OPENAI_API_KEY is not None:
        os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
    else:
        raise NoOpenAIToken("No OpenAI API token provided")
    pipeline = Pipeline(config_path=CONFIG_PATH)
    analisis = pipeline.get_analisis()
    print(colored(f'Candidato analizado : \n {pipeline.candidato}', 'cyan', attrs=["bold"]))
    print(colored(f'Respuesta del modelo : \n {analisis}', 'yellow', attrs=["bold"]))

if __name__ == '__main__':
    main()
    # terminal command : python main.py --config_path ./config/generate.json --token <tu_token>
    # executable command line : main.exe --config_path ./config/generate.json --token <tu_token>


