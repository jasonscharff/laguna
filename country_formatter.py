from bs4 import BeautifulSoup
import requests
import re
import json

def get_countries(filename):
    dictionary = {}
    with open(filename, 'r') as file:
        string = file.read()
        entries = string.split('\n')
        for entry in entries:
            soup = BeautifulSoup(entry, 'html.parser')
            link = soup.find('link')
            lang_code = link['hreflang']
            code = lang_code.split('-')[1]
            website = link['href']
            r = requests.get(website)
            regex = re.compile('\"site_currency\":\"(.*?)\"')
            match = regex.search(r.text)
            currency_code =  match.group(1)
            dictionary[code] = {'currency' : {'id' : currency_code}, 'kayak' : {'uri' : website}}

    with open('countries.json', 'w') as fp:
        json.dump(dictionary, fp)





get_countries('laguna_countries.txt')