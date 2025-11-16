import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from os import path, makedirs

# URL de la page BRVM
url = "https://www.brvm.org/fr/cours-actions/0"
# Use runner workspace for storage in GitHub Actions
path_folder_storage = "brvm-data"

''' Permet de récupérer les cours d'ouverture et clôture de brvm '''

response = requests.get(url, verify=False)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table')
table_cotation = tables[3]
rows = table_cotation.find_all('tr')

cotation_data = []

for row in rows[1:]:
    columns = row.find_all('td')
    if len(columns) > 1:
        cotation_date = datetime.now()
        ticker = columns[0].text.strip()
        nom_valeur = columns[1].text.strip()
        volume_transaction = columns[2].text.strip()
        open_cours = columns[4].text.strip()
        close_cours = columns[5].text.strip()
        variation = columns[6].text.strip()
        cotation_data.append((cotation_date, ticker, nom_valeur, volume_transaction, open_cours, close_cours, variation))

# Sauvegarder dans un fichier CSV
if not path.exists(path_folder_storage):
    makedirs(path_folder_storage)

filename = f"brvm_cours_{datetime.now().strftime('%Y%m%d')}.csv"
filename = path.join(path_folder_storage, filename)

with open(filename, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Date", "Symbole", "Nom", "Volume", "Cours ouverture", "Cours Cloture", "Variation"])
    writer.writerows(cotation_data)
