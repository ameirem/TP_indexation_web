import json
import argparse
from query_processor import QueryProcessor
from utils import load_json

def main():
    parser = argparse.ArgumentParser(description='Process query and operator.')
    parser.add_argument('query', nargs='?', help='Query string')
    parser.add_argument('-op', '--operator', choices=['AND', 'OR'], help='Operator (AND or OR)')

    args = parser.parse_args()

    if args.query:
        user_query = args.query
        operator = args.operator if args.operator else "AND"  # Par défaut, l'opérateur est 'AND'
    else:
        user_query = input("Entrez votre requête : ")
        operator = input("Entrez l'opérateur (OR/AND) : ") if input("Entrez l'opérateur (OR/AND) : ") else "AND"  # Par défaut, l'opérateur est 'AND'


    # Charger les données et les index depuis les fichiers JSON
    documents = load_json('data/documents.json')
    content_index = load_json('data/content_pos_index.json')
    title_index = load_json('data/title_pos_index.json')

    # Initialiser le QueryProcessor
    query_processor = QueryProcessor(documents, content_index, title_index)

    # Traiter la requête et obtenir les résultats
    results = query_processor.process_query(user_query, operator=operator)

    # Préparer les résultats au format JSON
    output_results = []

    if results:
        for result in results:
            doc_id, score = result
            # Récupérer le titre et l'URL du document
            doc_title = documents[int(doc_id)]['title']
            doc_url = documents[int(doc_id)]['url']
            # Ajouter le document à la liste de résultats
            output_results.append({"Titre": doc_title, "URL": doc_url})

    # Obtenir le nombre total de documents dans l'index
    total_documents = len(documents)
    # Obtenir le nombre de documents qui ont survécu au filtre
    filtered_documents_count = len(results)

    # Enregistrer les résultats au format JSON
    with open('results.json', 'w') as json_file:
        json.dump({"Resultats": output_results, "Total_documents": total_documents, "Documents_filtrés": filtered_documents_count}, json_file, indent=4)

    print("Les résultats ont été enregistrés dans 'results.json'.")

if __name__ == "__main__":
    main()

