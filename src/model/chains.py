import logging
import logging.config
import logging.handlers
from typing import List, Dict
from langchain.chains.llm import LLMChain
from langchain_core.output_parsers import JsonOutputParser,StrOutputParser
from .prompts import (
    analyze_cv_prompt,
    offer_check_prompt,
    re_analyze_cv_prompt,
    cv_check_prompt
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
    
    logger.info(f"Initializing analyzer chain ...")
    model = get_model()
    chain = prompt_template | model | parser()
    
    return chain

def get_reviewer_offer_chain( 
                get_model: callable = get_open_ai_json, 
                prompt_template: str = offer_check_prompt, 
                parser: JsonOutputParser = JsonOutputParser
              ) -> LLMChain:
    """Retorna la langchain chain para el agente revisor"""
    
    logger.info(f"Initializing reviewer chain ...")
    model = get_model()
    chain = prompt_template | model | parser()
    
    return chain

def get_re_analyzer_chain( 
                get_model: callable = get_open_ai_json, 
                prompt_template: str = re_analyze_cv_prompt, 
                parser: JsonOutputParser = JsonOutputParser
              ) -> LLMChain:
    """Retorna la langchain chain para el agente 're' analista"""
    
    logger.info(f"Initializing re analist chain chain ...")
    model = get_model()
    chain = prompt_template | model | parser()
    
    return chain

def get_reviewer_cv_chain( 
                get_model: callable = get_open_ai_json, 
                prompt_template: str = cv_check_prompt, 
                parser: JsonOutputParser = JsonOutputParser
              ) -> LLMChain:
    """Retorna la langchain chain para el agente revisor de alucionaciones iniciales"""
    
    logger.info(f"Initializing Hallucination agent chain ...")
    model = get_model()
    chain = prompt_template | model | parser()
    
    return chain
