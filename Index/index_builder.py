from collections import defaultdict
from nltk.tokenize import word_tokenize
from utils import save_json_file
from data_processing import apply_stemming


def build_non_positional_index(documents):
    # Initialize data structures for the index
    index = defaultdict(list)

    # Iterate through the documents and build the index
    for i, document in enumerate(documents):
        title = document['title']
        # Tokenize the title
        title_tokens = word_tokenize(title.lower())
        # Update the index
        for token in title_tokens:
            index[token].append(i)

    save_json_file(index,'title.non_pos_index.json')
    return index

   

def build_stemmed_index(documents):
    # Initialize data structures for the index
    index = defaultdict(list)

    # Iterate through the documents and build the index
    for i, document in enumerate(documents):
        title = document['title']
        # Apply stemming to the title
        stemmed_title = apply_stemming(title)

        # Tokenize the stemmed title
        title_tokens = word_tokenize(stemmed_title)

        # Update the index
        for token in title_tokens:
            index[token].append(i)
    
    # Write the index to a JSON file
    save_json_file(index,'mon_stemmer.title.non_pos_index.json')
    
def build_positional_index(data):
    pos_index = defaultdict(dict)
    for doc_id, doc in enumerate(data):
        title = doc['title']
        title_tokens = word_tokenize(title)

    # Parcours des tokens dans le titre
        for position, token in enumerate(title_tokens):
        # Ajout de l'entrée dans l'index positionnel
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
    # Création d'un index positionnel pour le contenu
    pos_index_content = defaultdict(dict)

# Parcours des documents
    for doc_id, doc in enumerate(data):
        content = doc['content']
        content_tokens = word_tokenize(content)

        # Parcours des tokens dans le contenu
        for position, token in enumerate(content_tokens):
            # Ajout de l'entrée dans l'index positionnel pour le contenu
            if token in pos_index_content:
                if doc_id in pos_index_content[token]:
                    pos_index_content[token][doc_id]['positions'].append(position)
                    pos_index_content[token][doc_id]['count'] += 1
                else:
                    pos_index_content[token][doc_id] = {'positions': [position], 'count': 1}
            else:
                pos_index_content[token] = {doc_id: {'positions': [position], 'count': 1}}

    save_json_file(pos_index_content,'content_pos_index.json')