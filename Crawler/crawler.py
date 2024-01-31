import multiprocessing
from bs4 import BeautifulSoup
from queue import Queue, Empty
from urllib.robotparser import RobotFileParser
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse
import requests
from xml.etree import ElementTree as ET
import sqlite3
from database import DatabaseManager

class Crawler:
    def __init__(self, seed_url, max_urls=250, max_urls_per_page=10, delay=3, num_threads=5, db_file='mywebpages.db'):
        """
        Initialise un nouvel objet Crawler.

        Args:
            seed_url (str): L'URL de départ pour le crawling.
            max_urls (int): Le nombre maximum d'URLs à crawler.
            max_urls_per_page (int): Le nombre maximum d'URLs à extraire par page.
            delay (int): Le délai entre chaque requête (en secondes).
            num_threads (int): Le nombre de threads à utiliser pour le crawling.
            db_file (str): Le nom du fichier de base de données SQLite.
        """
        self.seed_url = seed_url
        self.root_url = '{}://{}'.format(urlparse(self.seed_url).scheme, urlparse(self.seed_url).netloc)
        self.pool = ThreadPoolExecutor(max_workers=num_threads)  # Pool de threads pour les requêtes
        self.scraped_pages = set([])  # Ensemble de pages déjà visitées
        self.crawl_queue = Queue()  # File d'attente pour les URLs à visiter
        self.crawl_queue.put(self.seed_url)  # Ajoute l'URL initiale à la file d'attente
        self.max_urls = max_urls
        self.max_urls_per_page = max_urls_per_page
        self.delay = max(delay, 3)
        self.db_file = db_file
        self.db_manager = DatabaseManager(db_file=db_file)  # Gestionnaire de base de données
        self.db_manager.create_table()  # Crée la table dans la base de données

    def parse_links(self, html):
        """
        Analyse le HTML d'une page pour extraire les liens et les ajouter à la file d'attente.

        Args:
            html (str): Le contenu HTML de la page à analyser.
        """
        soup = BeautifulSoup(html, 'html.parser')
        anchor_tags = soup.find_all('a', href=True)
        links_added = 0  # Initialise un compteur pour les liens ajoutés

        for link in anchor_tags:
            if links_added >= self.max_urls_per_page:  # Vérifie si le max est atteint
                break  # Sort de la boucle si le maximum est atteint

            url = link['href']
            if url.startswith('/') or url.startswith(self.root_url):
                url = urljoin(self.root_url, url)
                if url not in self.scraped_pages:
                    self.crawl_queue.put_nowait(url)
                    links_added += 1  # Incrémente le compteur après l'ajout d'un lien

    def is_allowed(self, url):
        """
        Vérifie si l'accès à l'URL est autorisé par le fichier robots.txt.

        Args:
            url (str): L'URL à vérifier.

        Returns:
            bool: True si l'accès est autorisé, False sinon.
        """
        rp = RobotFileParser()
        rp.set_url(self.root_url + '/robots.txt')
        rp.read()
        return rp.can_fetch("*", url)

    def get_sitemap(self):
        """
        Récupère les URL de sitemap à partir du fichier robots.txt.

        Returns:
            list: Liste des URL de sitemap.
        """
        rp = RobotFileParser()
        rp.set_url(self.root_url + '/robots.txt')
        rp.read()
        return rp.site_maps()

    def read_sitemap(self, sitemap_url):
        """
        Lit le sitemap XML et ajoute les URLs à la file d'attente.

        Args:
            sitemap_url (str): L'URL du sitemap.
        """
        try:
            response = requests.get(sitemap_url)
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                for child in root:
                    if child.tag.endswith('url'):
                        loc = child.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
                        queue_contents = list(self.crawl_queue.queue)
                        if loc not in queue_contents:
                            self.crawl_queue.put(loc)
        except Exception as e:
            print("Error reading sitemap:", e)

    def scrape_info(self, html):
        """
        Récupère les informations pertinentes à partir du contenu HTML d'une page.

        Args:
            html (str): Le contenu HTML de la page à analyser.

        Returns:
            str: Le texte extrait de la page.
        """
        soup = BeautifulSoup(html, "html.parser")  # Analyse le HTML avec BeautifulSoup
        web_page_paragraph_contents = soup('p')  # Récupère tous les paragraphes
        text = ''
        for para in web_page_paragraph_contents:
            if not ('https:' in str(para.text)):
                text = text + str(para.text).strip()
        return text

    def post_scrape_callback(self, res):
        """
        Callback appelé après avoir récupéré le contenu HTML d'une page.

        Args:
            res: Le résultat de la requête asynchrone.
        """
        result = res.result()  # Récupère le résultat de la requête
        if result and result.status_code == 200:  # Si la requête a abouti
            url = result.url  # Récupère l'URL de la page crawlée
            content = self.scrape_info(result.text)  # Récupère les informations de la page
            self.parse_links(result.text)  # Analyse les liens sur la page
            self.db_manager.insert_page(url, content)  # Insère l'URL et le contenu dans la base de données

    def scrape_page(self, url):
        """
        Récupère le contenu HTML d'une page à partir de son URL.

        Args:
            url (str): L'URL de la page à récupérer.

        Returns:
            requests.Response: La réponse de la requête HTTP.
        """
        try:
            res = requests.get(url, timeout=self.delay)  # Effectue une requête GET avec le délai pour respecter la politeness
            return res
        except requests.RequestException:
            return

    def save_urls(self, url):
        """
        Sauvegarde les URLs crawlées dans un fichier.

        Args:
            url (str): L'URL à sauvegarder.
        """
        with open('crawled_webpages.txt', 'a') as file:
            file.write(url + '\n')

    def run(self):
        """
        Lance le web crawler en parcourant les URLs dans la file d'attente.
        """
        sitemap_urls = self.get_sitemap()
        if sitemap_urls:
            for sitemap in sitemap_urls:
                self.read_sitemap(sitemap)
            print('Sitemap found in robots.txt')
        while not self.crawl_queue.empty() and len(self.scraped_pages) < self.max_urls:
            try:
                target_url = self.crawl_queue.get(timeout=self.delay)  # Récupère une URL de la file d'attente
                if self.is_allowed(target_url) and target_url not in self.scraped_pages:
                    print("Scraping URL: {}".format(target_url))
                    self.scraped_pages.add(target_url)  # Ajoute l'URL à l'ensemble des pages visitées
                    job = self.pool.submit(self.scrape_page, target_url)  # Soumet la tâche de récupération de la page
                    job.add_done_callback(self.post_scrape_callback)  # Ajoute un callback pour le traitement
                    self.save_urls(target_url)
            except Empty:
                return
            except Exception as e:
                print(e)
                continue
        print(f'Number of pages scraped : {len(self.scraped_pages)}')


