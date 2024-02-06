from utils import load_json_file, calculate_statistics
from index_builder import build_content_pos_index,build_non_positional_index,build_positional_index,build_stemmed_index


def main():
    # Charger les données à partir du fichier JSON
    crawled_urls = load_json_file('crawled_urls.json')
    # Construire l'index non positionnel
    build_non_positional_index(crawled_urls)
    calculate_statistics(crawled_urls)
     # Construire l'index positionnel
    build_positional_index(crawled_urls)
     # Construire l'index non positionnel stemmé
    build_stemmed_index(crawled_urls)
     # Construire l'index positionnel basé sur le contenu des documents
    build_content_pos_index(crawled_urls)

if __name__ == "__main__":
    main()
