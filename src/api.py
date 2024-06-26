import os
import logging
from dotenv import load_dotenv
from model.utils import setup_logging
from backend.fast_api import run_fast_api

# Logging configuration
logger = logging.getLogger(__name__)

def main():
    
    # Load environment variables from .env file
    load_dotenv()

    # Set environment variables
    os.environ['LANGCHAIN_TRACING_V2'] = 'true'
    os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
    os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
    os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
    os.environ['NVIDIA_API_KEY'] = os.getenv('NVIDIA_API_KEY')
    os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')
    
    setup_logging()
    run_fast_api()
    
if __name__ == '__main__':
    main()


