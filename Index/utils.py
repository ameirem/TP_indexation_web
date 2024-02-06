import json
from nltk.tokenize import word_tokenize
from collections import defaultdict

def load_json_file(file_path):
    """
    Charge un fichier JSON à partir du chemin spécifié.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def save_json_file(data, file_path):
    """
    Enregistre des données au format JSON dans un fichier.
    """
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def calculate_statistics(documents):
    # Initialize data structures for the statistics
    total_tokens = 0
    num_documents = len(documents)
    token_counts = defaultdict(int)
    tokens_per_field = defaultdict(int)
    min_tokens = float('inf')
    max_tokens = 0

    # Iterate through the documents to calculate statistics
    for document in documents:
        title = document['title']
        content = document['content']
        url = document['url']
        h1 = document['h1']
        # Tokenize the fields
        title_tokens = word_tokenize(title.lower())
        content_tokens = word_tokenize(content.lower())
        url_tokens = word_tokenize(url.lower())
        h1_tokens = word_tokenize(h1.lower())
        # Update statistics for tokens per field
        tokens_per_field['title'] += len(title_tokens)
        tokens_per_field['content'] += len(content_tokens)
        tokens_per_field['url'] += len(url_tokens)
        tokens_per_field['h1'] += len(h1_tokens)
        # Update min and max tokens
        min_tokens = min(min_tokens, len(content_tokens))
        max_tokens = max(max_tokens, len(content_tokens))
        # Update token counts
        for token in title_tokens:
            token_counts[token] += 1

    total_tokens = sum(tokens_per_field.values())

    # Calculate average tokens per document
    avg_tokens_per_document = tokens_per_field['content'] / num_documents

    # Create statistics dictionary
    statistics = {
        'num_documents': num_documents,
        'total_tokens': total_tokens,
        'avg_tokens_per_document': avg_tokens_per_document,
        'tokens_per_field': tokens_per_field,
        'min_tokens': min_tokens,
        'max_tokens': max_tokens,
        'token_counts': token_counts
    }
    
    save_json_file(statistics,'metadata.json')
    return statistics


