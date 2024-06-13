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
from src.model.chains import get_analyzer_chain
from src.model.graph import create_graph, compile_workflow
from src.model.states import (
    Analisis,
    Candidato,
    State
)
from src.model.utils import (
                        get_current_spanish_date_iso, 
                        setup_logging,
                        get_id,
                        get_arg_parser
                        )
from src.backend.fast_api import run_fast_api
from src.model.exceptions import NoOpenAIToken, JsonlFormatError

# Load environment variables from .env file
load_dotenv()

# Set environment variables
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')


# Logging configuration
logger = logging.getLogger(__name__)

def main():
    setup_logging()
    run_fast_api()
    
    
if __name__ == '__main__':
    main()

