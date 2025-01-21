import os
import json
from PyQt5.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QComboBox,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QStackedWidget,
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My browser")
        self.setGeometry(500, 500, 800, 600)

        self.stack = QStackedWidget()  # Stack pour changer de page
        self.setCentralWidget(self.stack)

        self.init_ui()

    def init_ui(self):
        # Charger les moteurs de recherche depuis le JSON
        search_engines = self.load_search_engines()
        if not search_engines:
            QMessageBox.critical(self, "Erreur", "Aucun moteur de recherche trouvé.")
            return

        # Page d'accueil
        self.home_page = QWidget()
        home_layout = QVBoxLayout()
        self.home_page.setLayout(home_layout)
        home_layout.setAlignment(Qt.AlignCenter)
        self.stack.addWidget(self.home_page)

        # Menu déroulant pour les moteurs de recherche
        self.search_engine_selector = QComboBox()
        for engine in search_engines:
            logo_path = engine.get("logo", "")
            if os.path.exists(logo_path):
                icon = QIcon(logo_path)
            else:
                icon = QIcon()
            self.search_engine_selector.addItem(icon, engine["name"], engine["url"])
        home_layout.addWidget(self.search_engine_selector, alignment=Qt.AlignCenter)

        # Barre de recherche + bouton
        search_layout = QHBoxLayout()
        search_layout.setAlignment(Qt.AlignCenter)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Rechercher")
        self.search_bar.setFont(QFont("Arial", 14))
        self.search_bar.setFixedWidth(400)
        self.search_bar.returnPressed.connect(self.search)
        search_layout.addWidget(self.search_bar)

        search_button = QPushButton(QIcon("assets/search.svg"), "")
        search_button.setFixedSize(40, 40)
        search_button.clicked.connect(self.search)
        search_layout.addWidget(search_button)

        home_layout.addLayout(search_layout)

        # Page de résultats
        self.results_page = QWidget()
        results_layout = QVBoxLayout()
        self.results_page.setLayout(results_layout)
        self.results_view = QWebEngineView()
        results_layout.addWidget(self.results_view)

        self.stack.addWidget(self.results_page)

    def search(self):
        """
        Méthode déclenchée lors d'une recherche.
        Charge les résultats dans la vue Web de la page principale.
        """
        current_engine_url = self.search_engine_selector.currentData()
        query = self.search_bar.text().strip()

        if query:
            try:
                search_url = f"{current_engine_url}{query}"
                self.results_view.setUrl(QUrl(search_url))  # Charger l'URL dans la vue Web
                self.stack.setCurrentWidget(self.results_page)  # Changer de page
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Une erreur est survenue : {str(e)}")
        else:
            QMessageBox.warning(self, "Attention", "Le champ de recherche est vide.")

    def load_search_engines(self):
        """
        Charge la liste des moteurs de recherche depuis un fichier JSON.
        Retourne la liste vide en cas d'echec.
        """
        json_path = os.path.join("dummies", "search_engines.json")
        try:
            if not os.path.exists(json_path):
                QMessageBox.critical(self, "Erreur", f"Le fichier {json_path} est introuvable.")
                return []

            with open(json_path, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            QMessageBox.critical(self, "Erreur", "Erreur json format.")
            return []
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue : {str(e)}")
            return []
