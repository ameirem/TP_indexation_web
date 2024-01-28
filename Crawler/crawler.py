import requests
from urllib.parse import urlparse, urljoin
import urllib.request as request
import sqlalchemy
import urllib.robotparser
from bs4 import BeautifulSoup
import sqlite3

class MonCrawler():

    def __init__(self, seed, max_iter=50,depth=5):
        self.seed=seed
        self.url=seed
        self.frontier=[]
        self.discovered=[]
        self.rp= urllib.robotparser.RobotFileParser(seed)
        self.depth=depth
        self.max_url=max_iter
        #self.create_database()


    #def create_database(self):
    #    self.connection = sqlite3.connect("crawler/webpages.db")
    #    with self.connection:
    #        cursor = self.connection.cursor()
    #        cursor.execute("""
    #            CREATE TABLE IF NOT EXISTS webpages (
    #                id INTEGER PRIMARY KEY AUTOINCREMENT,
    #                url TEXT NOT NULL,
    #                content TEXT,
    #                age INTEGER ,
    #                
    #            )
    #       """)   

    #def insert_to_database(self, url, content):
    #    with self.connection:
    #        cursor = self.connection.cursor()
    #        cursor.execute("""
    #            INSERT INTO webpages (url, content)
    #            VALUES (?, ?)
    #        """, (url, content)) # VOIR COMMENT UPDATER L'ÂGE
     
    def read_robotstxt(self,url) :
        url_robot=urljoin(url,'/robots.txt')
        self.rp.set_url(url_robot)
        self.rp.read()

    def read_sitemaps(self,url):
        url_robot=urljoin(url,'/robots.txt')
        self.rp.set_url(url_robot)
        return self.rp.site_maps()
     

    def crawl_page(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                self.discovered.append(url)
                #self.write_to_file(url)
                links = [a['href'] for a in soup.find_all('a', href=True)]
                for link in links[:5]:
                    absolute_link = self.get_absolute_url(url, link)
                    if absolute_link not in self.frontier:
                        self.crawl_page(absolute_link)
        except Exception as e:
            print(f"Error crawling {url}: {str(e)}")




import os
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
from urllib import robotparser
from urllib.parse import urlparse, urljoin
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import xml.etree.ElementTree as ET



Base = declarative_base()

class Webpage(Base):
    __tablename__ = 'webpages'
    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    content = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

class SimpleCrawler:
    def __init__(self, start_url):
        self.start_url = start_url
        self.visited_urls = set()
        self.max_urls_per_page = 5
        self.max_total_urls = 50
        self.create_database()
        self.robot_parser = self.load_robot_txt(start_url)

    def create_database(self):
        engine = create_engine('sqlite:///crawler/webpages.db', echo=True)
        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)

    def load_robot_txt(self, base_url):
        robot_url = urljoin(base_url, "/robots.txt")
        rp = robotparser.RobotFileParser()
        rp.set_url(robot_url)
        rp.read()
        return rp

    def can_crawl(self, url):
        return self.robot_parser.can_fetch("*", url)

    def insert_to_database(self, url, content):
        session = self.Session()
        webpage = Webpage(url=url, content=content)
        session.add(webpage)
        session.commit()
        session.close()
        with open("crawler/crawled_webpages.txt", "a") as file:
           file.write(url + "\n")       
           

    def crawl_page(self, url):
        try:
            if self.can_crawl(url):
                response = requests.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    content = str(soup)
                    self.visited_urls.add(url)
                    self.insert_to_database(url, content)
                    links = [a['href'] for a in soup.find_all('a', href=True)]
                    for link in links[:self.max_urls_per_page]:
                        absolute_link = urljoin(url, link)
                        if absolute_link not in self.visited_urls:
                            self.crawl_page(absolute_link)
            else:
                print(f"Skipping {url} as per robots.txt")
        except Exception as e:
            print(f"Error crawling {url}: {str(e)}")

    def get_absolute_url(self, base_url, relative_url):
        return urljoin(base_url, relative_url)

    def run(self):
        # Lire le sitemap.xml si disponible
        sitemap_url = urljoin(self.start_url, "/sitemap.xml")
        sitemap_response = requests.get(sitemap_url)
        
        if sitemap_response.status_code == 200:
            sitemap_tree = ET.fromstring(sitemap_response.text)
            sitemap_urls = [loc.text for loc in sitemap_tree.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
            
            for sitemap_url in sitemap_urls:
                self.crawl_page(sitemap_url)

        # Crawler de la page initiale
        self.crawl_page(self.start_url)


if __name__ == "__main__":
    start_url = "https://ensai.fr/"
    crawler = SimpleCrawler(start_url)
    crawler.run()


