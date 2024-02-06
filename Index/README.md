# Projet de Construction d'Index

Ce projet vise à construire différents types d'index à partir d'un ensemble de documents web obtenus grâce à un crawler. Les types d'index incluent des index non positionnels, des index positionnels, des index non positionnels stemmés et un index positionnel pour le contenu des documents. Les index construits sont ensuite sauvegardés au format JSON pour une utilisation ultérieure.

## Organisation du Projet

Le projet est organisé en plusieurs fichiers, chacun ayant une fonction spécifique :

- **`index_builder.py`**: Ce fichier contient les fonctions pour construire les différents types d'index. Il inclut des fonctions pour construire un index non positionnel, un index non positionnel stemmé, un index positionnel, et un index positionnel pour le contenu des documents.

- **`utils.py`**: Ce fichier contient des fonctions utilitaires pour charger et sauvegarder des fichiers JSON, ainsi que pour effectuer des calculs statistiques sur les documents.

- **`data_processing.py`**: Ce fichier contient une fonction pour appliquer le stemming à un texte en français.

- **`main.py`**: Ce fichier est le point d'entrée du programme. Il charge les données à partir d'un fichier JSON, appelle les fonctions de construction d'index et de calcul de statistiques, puis sauvegarde les index construits et les statistiques dans des fichiers JSON.

## Explication des Fonctions Principales

- **`build_non_positional_index(documents)`**: Cette fonction construit un index non positionnel à partir des documents fournis. Elle tokenize les titres des documents et construit l'index en associant chaque token à la liste des documents dans lesquels il apparaît.

- **`build_stemmed_index(documents)`**: Cette fonction construit un index non positionnel stemmé en appliquant le stemming aux titres des documents avant de construire l'index. Elle utilise la fonction `apply_stemming` définie dans `data_processing.py`.

- **`build_positional_index(data)`**: Cette fonction construit un index positionnel à partir des titres des documents. Elle associe chaque token à la liste des documents dans lesquels il apparaît, ainsi qu'à la position de chaque occurrence dans le titre.

- **`build_content_pos_index(data)`**: Cette fonction construit un index positionnel pour le contenu des documents. Elle fonctionne de manière similaire à `build_positional_index`, mais elle utilise le contenu des documents au lieu des titres.

- **`apply_stemming(text)`**: Cette fonction applique le stemming à un texte en français en utilisant la bibliothèque NLTK.

## Exécution du Programme

Pour exécuter le programme, suivez ces étapes :

1. Assurez-vous d'avoir Python installé sur votre système.
2. Clonez le dépôt dans votre environnement local.
3. Installez les dépendances requises en exécutant `pip install -r requirements.txt`.
4. Placez les fichiers JSON contenant les documents web dans le répertoire du projet.
5. Exécutez le fichier `main.py` en utilisant la commande `python main.py`.

Le programme chargera les documents à partir du fichier JSON, construira les différents types d'index, calculera les statistiques sur les documents, puis sauvegardera les index et les statistiques dans des fichiers JSON.