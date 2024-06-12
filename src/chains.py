import logging
import logging.config
import logging.handlers
from typing import List, Dict
from langchain.chains.llm import LLMChain
from langchain_core.output_parsers import JsonOutputParser,StrOutputParser
from .prompts import (
    analyze_cv_prompt,
    review_prompt
    )
from .models import (
    get_open_ai_json,
    get_open_ai
)

# Logging configuration
logger = logging.getLogger(__name__)

def get_analyzer_chain( 
                get_model: callable = get_open_ai_json, 
                prompt_template: str = analyze_cv_prompt, 
                parser: JsonOutputParser = JsonOutputParser
              ) -> LLMChain:
    """Retorna la langchain chain para el agente analista"""
    
    logger.info(f"Initializing chain ...")
    model = get_model()
    chain = prompt_template | model | parser()
    
    return chain

def get_reviewer_chain( 
                get_model: callable = get_open_ai_json, 
                prompt_template: str = review_prompt, 
                parser: JsonOutputParser = JsonOutputParser
              ) -> LLMChain:
    """Retorna la langchain chain para el agente revisor"""
    
    logger.info(f"Initializing chain ...")
    model = get_model()
    chain = prompt_template | model | parser()
    
    return chain

