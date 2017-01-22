from bs4 import BeautifulSoup
import requests
import json
import marisa_trie
import csv

from airport import  Airport



def get_all_airports():
    all_airports = []
    char = 'A'
    for i in xrange(0,26):
        print char
        all_airports.extend(get_airports(char))
        char = chr(ord(char) + 1)
    #save to json file
    with open('airports.json', 'w') as fp:
        json.dump(all_airports, fp, encoding='utf8')




def get_airports(first_iata_letter):
    url = 'https://en.wikipedia.org/wiki/List_of_airports_by_IATA_code:_{}'.format(first_iata_letter)

    r = requests.get(url)
    if r.status_code == 200:
        pass
    else:
        print ('fail with first letter ' + first_iata_letter)

    return parse_page(r.text)





def parse_page(html):
    airports = []
    soup = BeautifulSoup(html, 'html.parser')
    table_headers = []

    for tx in soup.find('tr').find_all('th'):
        table_headers.append(tx.text.replace(unichr(160), '_').replace(' ', '_').lower())

    for row in soup.find_all('tr'):
        columns = row.find_all('td')
        if len(columns) == len(table_headers):
            airport = {}
            i = 0
            for element in columns:
                airport[table_headers[i]] = element.text
                i += 1

            airports.append(airport)

    return airports


def parse_ranking_csv(ranking_csv):
    dictionary = {}

    with open(ranking_csv) as file:
        reader = csv.DictReader(file)
        for row in reader:
            code = row['code']
            icao = code.split('_')[1]
            passengers = int(row['passengers'])
            #we have data from two sources. Use the higher version when the data overlaps
            if icao in dictionary:
                previous_passenger_count = dictionary[icao]
                if previous_passenger_count > passengers:
                    passengers = previous_passenger_count

            dictionary[icao] = passengers

    return dictionary





def generate_tries(json_file, ranking_csv):

    airport_coefficients = parse_ranking_csv(ranking_csv)

    with open(json_file, 'r') as airports_data:
        airports = json.load(airports_data, encoding='utf8')
        airports_data.close()

        airport_names = []
        airport_name_dictionary = {}

        airport_iata = []
        airport_iata_dictionary = {}

        airport_icao = []
        airport_icao_dictionary = {}

        for airport in airports:

            icao = str(airport['icao'])
            if icao in airport_coefficients:
                airport_object = Airport(airport_json=airport, popularity=airport_coefficients[icao])
            else:
                airport_object = Airport(airport_json=airport)

            airport_names.append(airport_object.name)
            airport_iata.append(airport_object.iata)
            airport_icao.append(airport_object.icao)

            airport_name_dictionary[airport_object.name] = airport_object
            airport_iata_dictionary[airport_object.iata] = airport_object
            airport_icao_dictionary[airport_object.icao] = airport_object


    airport_name_trie = marisa_trie.Trie(airport_names)
    airport_icao_trie = marisa_trie.Trie(airport_icao)
    airport_iata_trie = marisa_trie.Trie(airport_iata)

    #use unoptimized pickle because unicode.
    import pickle

    pickle.dump(airport_name_trie, open("serialized/airport_names_trie.p", "wb"))
    pickle.dump(airport_iata_trie, open("serialized/airport_iata_trie.p", "wb"))
    pickle.dump(airport_icao_trie, open("serialized/airport_icao_trie.p", "wb"))

    pickle.dump(airport_name_dictionary, open("serialized/airport_names_dictionary.p", "wb"))
    pickle.dump(airport_iata_dictionary, open("serialized/airport_iata_dictionary.p", "wb"))
    pickle.dump(airport_icao_dictionary, open("serialized/airport_icao_dictionary.p", "wb"))




generate_tries('raw_data/airports.json','raw_data/top_airports.csv')