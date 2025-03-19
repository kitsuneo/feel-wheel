import platform
import logging
import os

logger = logging.getLogger(__name__)

# support logpath for windows and linux
def get_platform():
    return platform.system()

def get_main_dir():
    return os.path.abspath(os.getcwd())

def get_logpath():
    return get_main_dir() + '/logs'

def logging_config():
    return logging.basicConfig(filename=get_logpath() + "/builtin_log",
                               encoding="utf-8",
                               filemode="a",
                               format="%(asctime)s - %(levelname)s - %(message)s",
                               datefmt='%Y-%m-%d %H:%M:%S',
                               level=logging.DEBUG)