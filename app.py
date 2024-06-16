import os
import logging
from termcolor import colored
from dotenv import load_dotenv
from src.model.graph import create_graph, compile_workflow
from src.model.modes import ConfigGraph, Pipeline
from src.model.utils import (
                        get_current_spanish_date_iso, 
                        setup_logging,
                        get_id,
                        get_arg_parser
                        )


# Load environment variables from .env file
load_dotenv()

# Set environment variables
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')


# Logging configuration
logger = logging.getLogger(__name__)


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
