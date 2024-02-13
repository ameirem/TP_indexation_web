# Projet de Classement des Requêtes

Ce projet offre un système de classement de documents en fonction des requêtes des utilisateurs. Il repose sur une analyse approfondie des contenus des articles et des critères de pertinence pour fournir des résultats précis et adaptés aux besoins des utilisateurs.

## Fonctionnalités

- **Lecture d'une requête de l'utilisateur** : Le système permet à l'utilisateur de soumettre une requête pour obtenir des résultats pertinents. Il peut egalement influer le filtrage en précisant un opérateur.
  
- **Filtrage des documents pertinents en fonction de la requête** : Les documents sont filtrés en fonction de la requête de l'utilisateur pour présenter uniquement les documents les plus pertinents. 

- **Création d'une fonction de classement linéaire pour ordonner les documents filtrés** : Les documents sont classés selon un score de pertinence calculé à l'aide de différents critères.

- **Renvoi des résultats au format JSON, incluant le nombre total de documents et le nombre de documents filtrés** : Les résultats sont présentés de manière structurée pour une consultation facile par l'utilisateur.

## Structure du Code

Le code est organisé en modules distincts pour une meilleure gestion et une plus grande modularité :

- **`ranking.py`** : Contient la fonction de classement permettant d'évaluer la pertinence des documents par rapport à la requête.

- **`query_processor.py`** : Implémente la logique de traitement des requêtes utilisateur, y compris la détection de la langue, le filtrage des documents et le classement final.

- **`utils.py`** : Propose des fonctions utilitaires pour le traitement des données telles que la tokenisation du texte et le chargement des données depuis des fichiers JSON.

- **`main.py`** : Point d'entrée de l'application où les utilisateurs peuvent saisir leurs requêtes et spécifier les opérateurs logiques.

## Méthode de Classement

Le score de classement d'un document est calculé en tenant compte de plusieurs facteurs :

- **BM25 pour le Titre et le Contenu** : Évalue le score BM25 pour le titre et le contenu de chaque document par rapport à la requête de l'utilisateur.

- **Nombre d'Occurrences des Tokens** : Intègre le nombre d'occurrences des tokens de la requête dans le document.

- **Similarité des Langues** : Accorde un bonus de score si la langue du document est similaire à celle de la requête.

La formule de calcul du score de classement est la suivante :

\[ \text{score} = \alpha \times \text{BM25 du Titre} + \beta \times \text{BM25 du Contenu} + \gamma \times \text{Nombre d'Occurences des Tokens} + \epsilon \times \text{Similarité des Langues} \]

- \(\alpha\), \(\beta\), \(\gamma\) et \(\epsilon\) sont des poids pour ajuster l'importance relative de chaque critère par rapport à la requête. 

- Le score final est une combinaison linéaire de ces facteurs, avec des pondérations adaptées pour chaque aspect du classement.

- Par défaut, nous accordons plus d'importance au score du titre qu'à celui du contenu. Ainsi, \(\alpha = 20\), \(\beta = 10\), \(\gamma = 10\), \(\epsilon = 20\).

- Les tokens ayant du sens sont uniquement considéré et non les stopwords.

## Utilisation

1. **Clonage du Projet** : Clonez ce dépôt dans votre environnement local.

2. **Installation des Dépendances** : Exécutez `pip install -r requirements.txt` pour installer toutes les dépendances nécessaires.

3. **Exécution du Programme** : Vous pouvez lancer le programme de deux manières : 
    - En exécutant le fichier `main.py` avec la commande `python main.py`. Vous serez alors invité à saisir votre requête et à spécifier l'opérateur logique (AND ou OR).
    - En exécutant le fichier `main.py` avec la commande `python main.py <requête> --operator <operateur>` ou `python main.py <requête> -op <operateur>`. L'opérateur par défaut est 'AND'. 
    
    Assurez-vous d'utiliser la commande `python3` selon votre interpréteur Python.

4. **Consultation des Résultats** : Une fois la requête traitée, les résultats seront stockés dans un fichier JSON (`results.json`). Chaque document est présenté avec son titre et son URL. Les résultats incluent également le nombre total de documents dans l'index et le nombre de documents filtrés.

## Remarques

- La détection automatique de la langue garantit des résultats précis et adaptés à une variété de requêtes. Nous avons effectué une analyse des langues de notre fichier contenant les documents, expliquant ainsi notre approche dans le code.

- Le système est conçu pour être extensible et peut être facilement adapté pour prendre en charge de nouvelles fonctionnalités et améliorations.

- Le fichier `results.json` dans notre dossier est le résultat de la requête 'guerre mondiale' avec l'opérateur 'AND' (python3 main.py 'guerre mondiale')