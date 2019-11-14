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

def get_dataframe_path():
    return root/config['RumourEval2019']['dataframes']


def get_badwords():
    return root/config['RumourEval2019']['badwords']

def get_negative_smileys():
    return root/config['RumourEval2019']['negative_smileys']

def get_positive_smileys():
    return root/config['RumourEval2019']['positive_smileys']


def get_word2vec_pretrain():
    return root/config['RumourEval2019']['word_embeddings']
