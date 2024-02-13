from langdetect import detect
from rank_bm25 import BM25Okapi
from nltk.corpus import stopwords

class RankingFunctions:
    @staticmethod
    def ranking_function(query, document, document_tokens, document_count, alpha, beta,gamma,eps, query_language):
        """
        Calcule le score de classement d'un document en fonction de la requête.

        Args:
            query (str): La requête de l'utilisateur.
            document (dict): Le document à classer.
            document_tokens (dict): Les tokens du titre et du contenu du document.
            document_count (int): Le nombre de documents dans l'index.
            alpha (float): Le poids pour le score du contenu du document.
            beta (float): Le poids pour le score du titre du document.
            query_language (str): La langue de la requête.

        Returns:
            float: Le score de classement du document.
        """
        # Détection de la langue du document
        doc_language = detect(document['content'])       

        # Définition des stopwords en fonction de la langue du document
        if doc_language == 'en':
            stop_words = set(stopwords.words('english'))
        elif doc_language == 'de':
            stop_words = set(stopwords.words('german'))
        elif doc_language == 'es':
            stop_words = set(stopwords.words('spanish'))
        else:
            # Si la langue du document est autre que l'anglais ou l'allemand, on la consider comme francaise
            stop_words = set(stopwords.words('french'))

        # Prétraitement des tokens du titre et du contenu en supprimant les stopwords
        title_tokens = [token for token in document_tokens['title'] if token not in stop_words]
        content_tokens = [token for token in document_tokens['content'] if token not in stop_words]

        # Calcul du score BM25 pour le titre
        bm25_title = BM25Okapi([title_tokens])
        title_score = bm25_title.get_scores(query)

        # Calcul du score BM25 pour le contenu
        bm25_content = BM25Okapi([content_tokens])
        content_score = bm25_content.get_scores(query)

        # Calcul du score pour la même langue
        same_language_score = 1 if doc_language == query_language else 0

        # Calcul du score total en utilisant les poids alpha et beta
        score = alpha * title_score + beta * content_score + same_language_score * gamma + document_count * eps

        return score[0]

