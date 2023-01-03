import requests
from bs4 import BeautifulSoup
from urllib import request
import re
import toml
from helpers import *
import os
from Importer import Importer


# Read local `config.toml` file.
config = toml.load('config.toml')

# Check if file exist
if not os.path.isfile(config["sqlite_path"]):
    open(config["sqlite_path"], 'w+').close()

importer = Importer(config["sqlite_path"])



# Make a request to the website
response = requests.get('https://www.bubt.edu.bd/home/result')

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

results = soup.find_all('a', attrs={'download': True})

for result in results:
    result_url = result['href']
    intake = re.findall("int_[0-9]+", result['href'])[0][4:]

    request.urlretrieve(result_url.replace(" ", "%20"), "result.pdf")
    firstId = getFirstId('result.pdf')
    print(firstId)

    if firstId:
        importer.start(int(firstId), intake)



importer.close()