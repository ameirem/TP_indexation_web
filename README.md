# TP1-Indexation_web
 
## Projet de Crawler Web (multi-threaded)
### Description

Ce projet implémente un crawler web multi-threaded afin de extraire des informations à partir de pages web. Le crawler est capable de parcourir un site web à partir d'une URL de départ, extraire les liens et le contenu pertinent des pages, et les stocker dans une base de données SQLite.
Contributeur :

    Ndèye Marième Mbaye - email : ndeye-marieme.mbaye@eleve.ensai.fr

### Fonctionnalités

    Parcours d'un site web à partir d'une URL de départ.
    Extraction des liens et du contenu pertinent des pages visitées.
    Respect des règles des fichiers robots.txt pour déterminer les pages à explorer.
    Gestion d'un sitemap pour découvrir de nouvelles pages.
    Stockage des informations extraites dans une base de données SQLite.
   


### Exécution du Code

    Assurez-vous d'avoir Python installé sur votre système.
    Clonez ce dépôt dans votre environnement local.
    Installez les dépendances requises en exécutant pip install -r requirements.txt.
    Exécutez le fichier main.py en utilisant la commande python main.py. (> python3 main.py)

### Remarques
    Dans notre projet, le fichier main.py tourne sur l'url de base qu'est 'https://ensai.fr/'. Une potentielle amélioration de notre projet aurait été de permettre à l'utilisateur de définir son url de base grâce à des librairies comme sysargv : > main.py 'url'
    Il faudrait alors s'assurer d'avoir les autorisations appropriées pour accéder au site web que vous souhaitez crawler.
    Les performances du crawler peuvent varier en fonction de la taille et de la complexité du site web.
    Notre database ne stocek pas l'âge de la page mais uniquement la date à laquelle elle a été scrappée.

### Explication du code

Pour mettre en place notre crawler, nous avons conçu une classe nommée `Crawler`. Cette classe est chargée de parcourir les pages web à partir d'une URL de départ. 

#### Initialisation et Paramètres

Lors de l'initialisation de la classe `Crawler`, plusieurs paramètres peuvent être configurés :

- **URL de départ (`seed_url`)** : L'URL à partir de laquelle le crawling commence.
- **Nombre maximum de pages à crawler (`max_urls`)** : Limite le nombre de pages que le crawler peut visiter. Par défaut est à 250
- **Nombre maximum d'URLs à extraire par page (`max_urls_per_page`)** : Limite le nombre d'URLs à extraire à partir de chaque page visitée.
- **Délai entre les requêtes (`delay`)** : Attente entre chaque requête pour éviter la surcharge des serveurs. Par défaut est à 3 et ne peut excéder 3 par politeness
- **Nombre de threads (`num_threads`)** : Contrôle le nombre de threads utilisés pour le crawling. Par défaut est à 5
- **Nom du fichier de la base de données SQLite (`db_file`)** : Spécifie le fichier de base de données dans lequel les informations des pages seront stockées. Par défaut est 'mywebpages'

#### Utilisation du Multi-threading

Pour améliorer l'efficacité du crawling, nous avons utilisé le multi-threading à l'aide de la classe `ThreadPoolExecutor`. Cela nous permet d'exécuter plusieurs tâches de récupération de page en parallèle, accélérant ainsi le processus de crawl.

#### Respect des Fichiers `robots.txt`

Le crawler respecte les directives des fichiers `robots.txt` en utilisant la classe `RobotFileParser` de la bibliothèque `urllib.robotparser`. Avant de crawler une page, le crawler vérifie d'abord si elle est autorisée à être visitée en fonction des règles spécifiées dans le fichier `robots.txt` du site.

#### Utilisation des Sitemaps

Le crawler explore également les sitemaps pour identifier de nouvelles pages à crawler. Il récupère les URLs à partir des sitemaps fournis par les sites web depuis le fichier robots.txt , permettant ainsi une exploration plus exhaustive et systématique du contenu.

#### Extraction et Stockage des Informations

Une fois qu'une page est crawlée avec succès, le crawler extrait les informations pertinentes à partir du contenu HTML de la page à l'aide de la bibliothèque `BeautifulSoup`. Ces informations sont ensuite stockées dans une base de données SQLite à l'aide de la classe `DatabaseManager`.

#### Gestion des Requêtes Concurrentes et Politesses du Crawler

Le crawler gère efficacement les requêtes concurrentes en utilisant des threads, mais il est également conçu pour éviter de surcharger les serveurs web. Il respecte les délais entre les requêtes et suit les directives des fichiers `robots.txt` pour maintenir des pratiques de crawl respectueuses et polites.