from utils import Tokenizer
from ranking import RankingFunctions
from langdetect import detect

class QueryProcessor:
    def __init__(self, documents, content_index, title_index):
        """
        Initialise un QueryProcessor avec les documents et les index.

        Args:
            documents (list): Une liste de documents.
            content_index (dict): Index des tokens dans le contenu des documents.
            title_index (dict): Index des tokens dans le titre des documents.
        """
        self.documents = documents
        self.content_index = content_index
        self.title_index = title_index

    def process_query(self, query, operator="AND"):
        """
        Traite la requête de l'utilisateur et renvoie les documents filtrés et classés.

        Args:
            query (str): La requête de l'utilisateur.
            operator (str): L'opérateur de recherche (AND ou OR). Par défaut, AND.

        Returns:
            list: Une liste de tuples (doc_id, score) pour les documents classés.
        """
        # Détecter la langue de la requête
        query_language = detect(query)
        
        # Tokeniser la requête
        query_tokens = Tokenizer.tokenize(query)
        
        # Filtrer les documents en fonction de la requête
        content_filtered_documents = self.filter_documents(query_tokens, self.content_index, operator)
        
        # Classer les documents filtrés
        ranked_documents = self.rank_documents(query_tokens, content_filtered_documents, query_language)

        return ranked_documents

    def filter_documents(self, tokens, index, operator="AND"):
        """
        Filtrer les documents en fonction des tokens de la requête.

        Args:
            tokens (list): Liste des tokens de la requête.
            index (dict): Index des tokens dans les documents.
            operator (str): L'opérateur de recherche (AND ou OR).

        Returns:
            dict: Dictionnaire des documents filtrés avec leurs comptes de tokens.
        """
        filtered_documents = {}

        if operator.upper() == "OR":
            # Si l'opérateur est OR, ajouter les documents contenant au moins un des tokens
            for token in tokens:
                if token in index:
                    for doc_id, doc_info in index[token].items():
                        if doc_id not in filtered_documents:
                            filtered_documents[doc_id] = doc_info["count"]
                        else:
                            filtered_documents[doc_id] += doc_info["count"]

        elif operator.upper() == "AND":
            # Si l'opérateur est AND, ajouter les documents contenant tous les tokens
            documents_sets = [set(index[token].keys()) for token in tokens if token in index]

            if documents_sets:
                common_documents = set.intersection(*documents_sets)
                for doc_id in common_documents:
                    total_count = sum(index[token][doc_id]["count"] for token in tokens if doc_id in index[token])
                    filtered_documents[doc_id] = total_count

        return filtered_documents

    def rank_documents(self, query, doc_id_count, query_language):
        """
        Classer les documents filtrés en fonction de la requête.

        Args:
            query (str): La requête de l'utilisateur.
            doc_id_count (dict): Dictionnaire des documents filtrés avec leurs comptes de tokens.
            query_language (str): La langue de la requête.

        Returns:
            list: Une liste de tuples (doc_id, score) pour les documents classés.
        """
        # Classer les documents en utilisant une fonction de ranking personnalisée
        ranked_documents = []

        for doc_id in doc_id_count.keys():
            for doc in self.documents:
                if str(doc['id']) == str(doc_id):
                    content_tokens = Tokenizer.tokenize(doc['content'])
                    title_tokens = Tokenizer.tokenize(doc['title'])
                    doc_tokens = {'content': content_tokens, 'title': title_tokens}
                    score = RankingFunctions.ranking_function(query, doc, doc_tokens, doc_id_count[doc_id], alpha=20, beta=10,gamma=10,eps=20, query_language=query_language)
                    ranked_documents.append((doc_id, score))

        ranked_documents.sort(key=lambda x: x[1], reverse=True)

        return ranked_documents





