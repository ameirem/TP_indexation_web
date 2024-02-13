import json
from nltk.tokenize import word_tokenize



class Tokenizer:
    @staticmethod
    def tokenize(text):
        """
        Tokenize le texte en mots.

        Args:
            text (str): Le texte à tokeniser.

        Returns:
            list: Une liste de mots tokenisés par split et en minuscules.
        """
        return word_tokenize(text.lower())
    
def load_json(file_path):
    with open(file_path, 'r') as f:
        index = json.load(f)
    return index