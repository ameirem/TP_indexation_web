from collections import defaultdict
from nltk.tokenize import word_tokenize
from utils import save_json_file
from data_processing import apply_stemming


def build_non_positional_index(documents):
    # On initialise les structures de données pour l'index
    index = defaultdict(list)

    # On parcourt les documents et on construit l'index
    for i, document in enumerate(documents):
        title = document['title']
        # On tokenise le titre
        title_tokens = word_tokenize(title.lower())
        # On met à jour l'index
        for token in title_tokens:
            index[token].append(i)

    save_json_file(index,'title.non_pos_index.json')
    return index

   

def build_stemmed_index(documents):
    # On initialise les structures de données pour l'index
    index = defaultdict(list)

    # On parcourt les documents et on construit l'index
    for i, document in enumerate(documents):
        title = document['title']
        # On applique le stemming au titre
        stemmed_title = apply_stemming(title)

        # On tokenise le titre stemmé
        title_tokens = word_tokenize(stemmed_title)

        # On met à jour l'index
        for token in title_tokens:
            index[token].append(i)
    
    # On écrit l'index dans un fichier JSON
    save_json_file(index,'mon_stemmer.title.non_pos_index.json')
    
def build_positional_index(data):
    pos_index = defaultdict(dict)
    for doc_id, doc in enumerate(data):
        title = doc['title']
        title_tokens = word_tokenize(title)

    # On parcourt les tokens dans le titre
        for position, token in enumerate(title_tokens):
        # On ajoute l'entrée dans l'index positionnel
            if token in pos_index:
                if doc_id in pos_index[token]:
                    pos_index[token][doc_id]['positions'].append(position)
                    pos_index[token][doc_id]['count'] += 1
                else:
                    pos_index[token][doc_id] = {'positions': [position], 'count': 1}
            else:
                pos_index[token] = {doc_id: {'positions': [position], 'count': 1}}
    
    save_json_file(pos_index,'title.pos_index.json')


def build_content_pos_index(data):
    # On crée un index positionnel pour le contenu
    pos_index_content = defaultdict(dict)

# On parcourt les documents
    for doc_id, doc in enumerate(data):
        content = doc['content']
        content_tokens = word_tokenize(content)

        # On parcourt les tokens dans le contenu
        for position, token in enumerate(content_tokens):
            # On ajoute l'entrée dans l'index positionnel pour le contenu
            if token in pos_index_content:
                if doc_id in pos_index_content[token]:
                    pos_index_content[token][doc_id]['positions'].append(position)
                    pos_index_content[token][doc_id]['count'] += 1
                else:
                    pos_index_content[token][doc_id] = {'positions': [position], 'count': 1}
            else:
                pos_index_content[token] = {doc_id: {'positions': [position], 'count': 1}}

    save_json_file(pos_index_content,'content_pos_index.json')
