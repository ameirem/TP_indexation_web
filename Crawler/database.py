import sqlite3

class DatabaseManager:
    def __init__(self, db_file='mywebpages.db'):
        """
        Initialise un objet DatabaseManager.

        Args:
            db_file (str): Le nom du fichier de base de données SQLite.
        """
        self.db_file = db_file
        self.conn = None
        self.cursor = None
        self.connect()  # Établit la connexion à la base de données lors de l'initialisation

    def connect(self):
        """
        Établit une connexion à la base de données et crée la table si elle n'existe pas.
        """
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """
        Crée la table 'pages' dans la base de données si elle n'existe pas déjà.
        """
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS pages (
                            id INTEGER PRIMARY KEY,
                            url TEXT NOT NULL UNIQUE,
                            content TEXT,
                            age TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        self.conn.commit()

    def insert_page(self, url, content):
        """
        Insère une nouvelle page dans la table 'pages' de la base de données.

        Args:
            url (str): L'URL de la page.
            content (str): Le contenu de la page.
        """
        # Crée une nouvelle connexion pour chaque opération d'insertion
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO pages (url, content) VALUES (?, ?)", (url, content))
            conn.commit()
        except sqlite3.IntegrityError:
            pass  # Ignore les entrées en double
        finally:
            conn.close()  

    def close(self):
        """
        Ferme la connexion à la base de données.
        """
        self.conn.close()
