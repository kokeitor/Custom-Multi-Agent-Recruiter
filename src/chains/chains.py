import logging
import logging.config
import logging.handlers
from typing import List, Dict
from langchain.chains.llm import LLMChain
from langchain_core.output_parsers import JsonOutputParser,StrOutputParser
from prompts.prompts import (
    analyze_cv
    )
from models.models import (
    get_open_ai_json,
    get_open_ai
)

# Logging configuration
logger = logging.getLogger("Chains")

def get_chain( 
                get_model: callable = get_open_ai_json, 
                prompt_template: str = analyze_cv, 
                parser: JsonOutputParser = JsonOutputParser
              ) -> LLMChain:
    """Retorna la langchain chain"""
    
    logger.info(f"Initializing chain ...")
    model = get_model()
    chain = prompt_template | model | parser()
    
    return chain
