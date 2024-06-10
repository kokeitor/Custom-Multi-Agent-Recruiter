import os
import json
import pytz
import uuid
import logging
import logging.config
import logging.handlers
from datetime import datetime, timezone
from dataclasses import dataclass
from typing import Dict, List, Tuple, Union, Optional, Callable, ClassVar

# UTIL FUNCTIONS MODULE
def setup_logging() -> None:
    """
    Function to get root parent configuration logger.
    Child logger will pass info, debugs... log objects to parent's root logger handlers
    """
    CONFIG_LOGGER_FILE = os.path.join(os.path.abspath("./config"), "logger.json")
    
    with open(CONFIG_LOGGER_FILE, encoding='utf-8') as f:
        content = json.load(f)
    logging.config.dictConfig(content)

def get_current_spanish_date_iso():
    # Get the current date and time in the Europe/Madrid time zone
    spanish_tz = pytz.timezone('Europe/Madrid')
    return datetime.now(spanish_tz).strftime("%Y%m%d%H%M%S")

def get_id() -> str:
    return str(uuid.uuid4())