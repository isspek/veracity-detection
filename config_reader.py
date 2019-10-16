from configparser import ConfigParser
from pathlib import Path


def get_project_root() -> Path:
    """Returns project root folder."""
    return Path(__file__).parent


root = get_project_root()
config = ConfigParser()
config.read(root/'config.ini')


def get_final_key():
    return root/config['RumourEval2019']['final-key']
