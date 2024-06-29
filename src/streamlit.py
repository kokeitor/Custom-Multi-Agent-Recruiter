import os
import logging
from dotenv import load_dotenv
from model.utils import (
                        setup_logging,
                        )
from app.chatbot import run_app

# Logging configuration
logger = logging.getLogger(__name__)


def main() -> None:
    
    # Load environment variables from .env file
    load_dotenv()

    # Set environment variables
    os.environ['LANGCHAIN_TRACING_V2'] = 'true'
    os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
    os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
    os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
    os.environ['NVIDIA_API_KEY'] = os.getenv('NVIDIA_API_KEY')
    os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')

    # Logger set up
    setup_logging()
    
    logger.info(f"Streamlit app mode")

    CONFIG_PATH = os.path.join(os.path.dirname(__file__),'..', 'config', 'generation.json')
    logger.info(f"{CONFIG_PATH=}")
    
    # Run streamlit app
    run_app(config_graph_path=CONFIG_PATH)
    
if __name__ == '__main__':
    main()