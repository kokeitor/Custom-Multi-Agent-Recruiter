import os
import json
import pytz
import uuid
import argparse
import logging
import logging.config
import logging.handlers
from datetime import datetime
from typing import Dict, List, Tuple, Union, Optional, Callable, ClassVar

# Logging configuration
logger = logging.getLogger(__name__)

# UTIL FUNCTIONS MODULE
def setup_logging() -> None:
    """
    Function to get root parent configuration logger.
    Child logger will pass info, debugs... log objects to parent's root logger handlers
    """
    CONFIG_LOGGER_FILE = os.path.join(os.path.dirname(__file__), '..','..', 'config', 'logger.json') 
    logger.info(f"CONFIG_LOGGER_FILE -> {CONFIG_LOGGER_FILE}")

    with open(CONFIG_LOGGER_FILE, encoding='utf-8') as f:
        content = json.load(f)
    logging.config.dictConfig(content)
    
def get_current_spanish_date_iso():
    """Get the current date and time in the Europe/Madrid time zone"""
    spanish_tz = pytz.timezone('Europe/Madrid')
    return str(datetime.now(spanish_tz).strftime("%Y-%m-%d %H:%M:%S"))

def get_id() -> str:
    return str(uuid.uuid4())

def get_arg_parser() -> argparse.ArgumentParser:
    """
    Parse and create the console script input arguments
    Returns:
        argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser( 
                    prog='Analisis Cvs',
                    description='Obten un analisis del Cv segun la oferta de empleo deseada usando LLms')
    parser.add_argument('--data_path', type=str, required=False, help='Ruta del archivo de datos con el cv y oferta [json format]')
    parser.add_argument('--token', type=str, required=False, help='Token de conexion API openAI')
    parser.add_argument('--mode', type=str, required=True, help='Modo de generacion : "graph" "pipeline" ')
    parser.add_argument('--config_path', type=str, required=False, help='Ruta del archivo de configuracion [json format]')
    
    return parser


def get_current_spanish_date_iso_file_name_format():
    """Get the current date and time in the Europe/Madrid time zone"""
    spanish_tz = pytz.timezone('Europe/Madrid')
    return str(datetime.now(spanish_tz).strftime("%Y%m%d%H%M%S"))