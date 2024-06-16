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
from .chains import get_chain
from .prompts import (
    analyze_cv_prompt,
    offer_check_prompt,
    re_analyze_cv_prompt,
    cv_check_prompt,
    analyze_cv_prompt_nvidia,
    offer_check_prompt_nvidia,
    re_analyze_cv_prompt_nvidia,
    cv_check_prompt_nvidia
    )
from .graph import create_graph, compile_workflow
from .states import (
    Analisis,
    Candidato,
    State,
    Agent
)
from .utils import (
                        get_current_spanish_date_iso, 
                        setup_logging,
                        get_id,
                        get_arg_parser
                        )
from .exceptions import NoOpenAIToken, JsonlFormatError
from .models import (
    get_nvdia,
    get_ollama,
    get_open_ai_json,
    get_open_ai
)

# Load environment variables from .env file
load_dotenv()

# Set environment variables
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')


# Logging configuration
logger = logging.getLogger(__name__)


@dataclass()
class Pipeline:
    data_path: Optional[str] = None
    data: Optional[dict] = None
    
    def __post_init__(self):
        if self.data is not None and self.data_path is not None:
            logger.warning("Definidas dos configuraciones [archivo json y dict] -> da prioridad a dict config")
        if self.data is None and self.data_path is not None:
            self.data = self.get_data()
            logger.info(f"Definida configuracion mediante archivo JSON en {self.data_path}")
        if self.data is None and self.data_path is None:
            logger.exception("No se ha proporcionado ninguna configuración para la generación usando Pipeline")
            raise AttributeError("No se ha proporcionado ninguna configuración para la generación usando Pipeline")
        
        self.chain = get_chain(prompt_template=analyze_cv_prompt,get_model=get_open_ai)  # Get objeto base chain para la tarea de análisis de CVs
        if len(self.data) > 0:
            self.candidatos = [self.get_candidato(cv=candidato.get("cv", None), oferta=candidato.get("oferta", None)) for candidato in self.data]
        else:
            logger.exception("No se han proporcionado candidatos en el archivo jsonl con el correcto fomato [ [cv : '...', oferta : '...'] , [...] ] ")
            raise JsonlFormatError()
    
    def get_data(self) -> List[Dict[str,str]]:
        if not os.path.exists(self.data_path):
            logger.exception(f"Archivo de configuración no encontrado en {self.data_path}")
            raise FileNotFoundError(f"Archivo de configuración no encontrado en {self.data_path}")
        with open(file=self.data_path, mode='r', encoding='utf-8') as file:
            logger.info(f"Leyendo candidatos en archivo : {self.data_path} : ")
            try:
                data = json.load(file)
            except Exception as e:
                logger.exception(f"Error decoding JSON : {e}")
        return data
            
    def get_candidato(self, cv :str , oferta :str) -> Candidato:
        return Candidato(id=get_id(), cv=cv, oferta=oferta)

    def get_analisis(self) -> List[Analisis]:
        """Run Pipeline -> Invoca langchain chain -> genera objeto Analisis con respuesta del modelo"""
        analisis = []
        for candidato in self.candidatos:
            logger.info(f"Análisis del candidato : \n {candidato}")
            raw_response = self.chain.invoke(input={"cv": candidato.cv, "oferta": candidato.oferta})  # Invoca a la chain que parsea la respuesta del modelo a python dict
            logger.info(f"Análisis del modelo : \n {raw_response}")
            # Manejo de una respuesta del modelo en un formato no correcto [no alineado con pydantic BaseModel]
            try:
                analisis.append(Analisis(**raw_response,fecha=get_current_spanish_date_iso(),id=candidato.id , status="OK")) # Instancia de Pydantic Analisis BaseModel object
            except ValidationError as e:
                logger.exception(f'{e} : Formato de respuesta del modelo incorrecta')
                analisis.append(Analisis(puntuacion=0, experiencias=[{"error":"error"}],fecha=get_current_spanish_date_iso(),id=candidato.id, descripcion="", status="ERROR"))
        return analisis
        
@dataclass()
class ConfigGraph:
    MODEL : ClassVar = {
            "OPENAI": get_open_ai_json,
            "NVIDIA": get_nvdia,
            "OLLAMA": get_ollama
            }

    AGENTS : ClassVar = {
            "analyzer": Agent("analyzer","OPENAI",get_open_ai_json,0.0, analyze_cv_prompt),
            "re_analyzer": Agent("re_analyzer","OPENAI",get_open_ai_json,0.0, re_analyze_cv_prompt),
            "cv_reviewer": Agent("cv_reviewer","OPENAI",get_open_ai_json,0.0, cv_check_prompt),
            "offer_reviewer": Agent("offer_reviewer","OPENAI",get_open_ai_json,0.0, offer_check_prompt)
            }
    
    config_path: Optional[str] = None
    data_path: Optional[str] = None
    
    def __post_init__(self):
        if self.config_path is None:
            logger.exception("No se ha proporcionado ninguna configuración para la generación usando Agents")
            raise AttributeError("No se ha proporcionado ninguna configuración para la generación usando Agents")
        if self.data_path is None:
            logger.exception("No se han proporcionado datos para analizar para la generación usando Agents")
            raise AttributeError("No se han proporcionado datos para analizar para la generación usando Agents")
        if self.config_path is not None:
            self.config = self.get_config()
            logger.info(f"Definida configuracion mediante archivo JSONL en {self.config_path}")
        if self.config_path is not None:
            self.data = self.get_data()
            logger.info(f"Definidos los datos mediante archivo JSONL en {self.data_path}")
        
        if len(self.data) > 0:
            self.candidatos = [self.get_candidato(cv=candidato.get("cv", None), oferta=candidato.get("oferta", None)) for candidato in self.data]
        else:
            logger.exception("No se han proporcionado candidatos en el archivo jsonl con el correcto fomato [ [cv : '...', oferta : '...'] , [...] ] ")
            raise JsonlFormatError()
        
        # Graph Agents configuration
        self.agents_config = self.config.get("agents", None)
        if self.agents_config is not None:
            self.agents = self.get_agents()

        # Graph configuration
        self.iteraciones = self.config.get("iteraciones", len(self.candidatos))
        self.thread_id = self.config.get("thread_id", "4")
        self.verbose = self.config.get("verbose", 0)
        
    def get_config(self) -> dict:
        if not os.path.exists(self.config_path):
            logger.exception(f"Archivo de configuración no encontrado en {self.config_path}")
            raise FileNotFoundError(f"Archivo de configuración no encontrado en {self.config_path}")
        with open(self.config_path, encoding='utf-8') as file:
            config = json.load(file)
        return config
    
    def get_data(self) -> List[Dict[str,str]]:
        if not os.path.exists(self.data_path):
            logger.exception(f"Archivo de configuración no encontrado en {self.data_path}")
            raise FileNotFoundError(f"Archivo de configuración no encontrado en {self.data_path}")
        with open(file=self.data_path, mode='r', encoding='utf-8') as file:
            logger.info(f"Leyendo candidatos en archivo : {self.data_path} : ")
            try:
                data = json.load(file)
            except Exception as e:
                logger.exception(f"Error decoding JSON : {e}")
        return data
    
    def get_agents(self) -> Dict[str,Agent]:
        agents = ConfigGraph.AGENTS.copy()
        for agent_graph in agents.keys():
            for agent, agent_config in self.agents_config.items():
                if agent_graph == agent:
                    model_name = agent_config.get("name", None)
                    model_temperature = agent_config.get("temperature", 0.0)
                    if model_name is not None:
                        get_model = ConfigGraph.MODEL.get(model_name, None)
                        if get_model is None:
                            logger.error(f"The Model defined for agemt : {agent} isnt't available -> using OpenAI model")
                            get_model = get_open_ai
                            prompt = self.get_model_agent_prompt(model_name ='OPENAI', agent = agent)
                        else:
                            prompt = self.get_model_agent_prompt(model_name = model_name, agent = agent)
                            
                    else:
                        get_model = get_open_ai(temperature=model_temperature)

                    agents[agent] = Agent(
                        agent_name=agent,
                        model_name=model_name,
                        model=get_model,
                        temperature=model_temperature,
                        prompt=prompt
                    )
                else:
                    pass
        logger.info(f"Graph Agents : {agents}")
        return agents

    def get_model_agent_prompt(self, model_name : str, agent : str) -> PromptTemplate:
        if model_name == 'OPENAI':
            if agent == "analyzer":
                return analyze_cv_prompt
            elif agent == "re_analyzer":
                return re_analyze_cv_prompt            
            elif agent == "cv_reviewer":
                return cv_check_prompt        
            elif agent == "offer_reviewer":
                return offer_check_prompt
        elif model_name == 'NVIDIA' or  model_name =='OLLAMA':
            if agent == "analyzer":
                return analyze_cv_prompt_nvidia
            elif agent == "re_analyzer":
                return re_analyze_cv_prompt_nvidia            
            elif agent == "cv_reviewer":
                return cv_check_prompt_nvidia      
            elif agent == "offer_reviewer":
                return offer_check_prompt_nvidia
        else:
            return None

    def get_candidato(self, cv :str , oferta :str) -> Candidato:
        return Candidato(id=get_id(), cv=cv, oferta=oferta)
        
        

def main() -> None:
    # Logger set up
    setup_logging()
    
    # With scripts parameters mode
    parser = get_arg_parser()
    args = parser.parse_args()
    CONFIG_PATH = args.config_path
    OPENAI_API_KEY = args.token
    DATA_PATH = args.data_path
    MODE = args.mode
    
    # Without scripts parameters mode
    if OPENAI_API_KEY:
        os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
    else:
        os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
    if not CONFIG_PATH:
        CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config', 'generation.json') 
    if not DATA_PATH:
        DATA_PATH = os.path.join(os.path.dirname(__file__), 'config', 'data.json') 
    if not MODE:
        MODE = 'graph'
        
    logger.info(f"{DATA_PATH=}")
    logger.info(f"{CONFIG_PATH=}")
    logger.info(f"{MODE=}")
    
    # Mode -> Langgraph or One-shot [Pipeline]
    if MODE == 'graph':
        
        logger.info(f"Graph mode")
        logger.info(f"Getting Data and Graph configuration from {DATA_PATH=} and {CONFIG_PATH=} ")
        config_graph = ConfigGraph(config_path=CONFIG_PATH, data_path=DATA_PATH)
        
        logger.info("Creating graph and compiling workflow...")
        graph = create_graph(config=config_graph)
        workflow = compile_workflow(graph)
        logger.info("Graph and workflow created")
        
        thread = {"configurable": {"thread_id": config_graph.thread_id}}
        iteraciones = {"recursion_limit": config_graph.iteraciones}
        
        # itera por todos los candidatos definidos
        for candidato in config_graph.candidatos:
            input_candidato = {"candidato": candidato}
            logger.info(f"Start analisis for {candidato=}")
            logger.debug(f"Cv Candidato -> {candidato.cv}")
            logger.debug(f"Oferta de Empleo para candidato-> {candidato.oferta}")
            for event in workflow.stream(
                input_candidato, iteraciones
                ):
                if config_graph.verbose == 1:
                    print(colored(f"\nState Dictionary: {event}" ,  'cyan'))
                    
    if MODE == 'pipeline':
        logger.info(f"Pipeline mode")
        logger.info(f"Getting Data and Graph configuration from {DATA_PATH=} and {CONFIG_PATH=} ")
        pipeline = Pipeline(data_path=DATA_PATH)
        analisis = pipeline.get_analisis()
        for i,a in enumerate(analisis):
            print(colored(f'\n**CANDIDATO **\n- CV : \n{pipeline.candidatos[i].cv}\n- Oferta : {pipeline.candidatos[i].oferta} ', 'cyan', attrs=["bold"]))
            print(colored(f"\n**ANALISIS** 📝\n\nFecha del analisis : {a.fecha}\n- Puntuacion : {a.puntuacion}\n- Experiencias : {a.experiencias}\n- Descripcion : {a.descripcion}", 'light_yellow',attrs=["bold"]))

if __name__ == '__main__':
    main()
    # terminal command with script parameters : python app.py --data_path ./config/data.json --token <tu_token> --mode "graph" --config_path ./config/generation.json
    # terminal command : python app.py 
