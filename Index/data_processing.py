from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer

def apply_stemming(text):
    """
    Applique le stemming à un texte donné en français.
    """
    stemmer = SnowballStemmer("french", ignore_stopwords=True)
    tokens = word_tokenize(text.lower())
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    return " ".join(stemmed_tokens)