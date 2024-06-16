import logging
from langchain_openai import ChatOpenAI
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_community.chat_models import ChatOllama


# Logging configuration
logger = logging.getLogger(__name__)


def get_open_ai(temperature=0, model='gpt-3.5-turbo'):
    """
    _summary_
    Args:
        temperature (int, optional): _description_. Defaults to 0.
        model (str, optional): _description_. Defaults to 'gpt-3.5-turbo'.
    """
    logger.info(f"Using Open AI : {model}")
    llm = ChatOpenAI(
                    model=model,
                    temperature = temperature,
                    )
    return llm

def get_open_ai_json(temperature=0, model='gpt-3.5-turbo'):
    """
    _summary_
    Args:
        temperature (int, optional): _description_. Defaults to 0.
        model (str, optional): _description_. Defaults to 'gpt-3.5-turbo'.
    """
    logger.info(f"Using Open AI : {model}")
    llm = ChatOpenAI(
                    model=model,
                    temperature = temperature,
                    model_kwargs={"response_format": {"type": "json_object"}},
                    )
    return llm

def get_nvdia(temperature=0, model='meta/llama3-70b-instruct'):
    """
    Nvidia llama 3 model
    Args:
        temperature (int, optional): _description_. Defaults to 0.
        model (str, optional): _description_.
    """
    logger.info(f"Using NVIDIA : {model}")
    llm = ChatNVIDIA(
                    model=model,
                    temperature = temperature
                    )
    return llm

def get_ollama(temperature=0, model='llama3'):
    """
    Ollama local model
    Args:
        temperature (int, optional): _description_. Defaults to 0.
        model (str, optional): _description_.
    """
    logger.info(f"Using Ollama : {model}")
    llm = ChatOllama(
                    model=model,
                    temperature = temperature,
                    format="json"
                    )
    return llm