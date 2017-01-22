from flask import Flask
import requests
import json
import pickle
import marisa_trie
from flask import Response, request
from airport import Airport
from flask_cors import CORS, cross_origin



app = Flask(__name__)

MAX_SUGGESTIONS = 5

import os
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')

airport_name_trie = pickle.load(open(os.path.join(APP_STATIC, "airport_names_trie.p"), "rb" ) )
airport_iata_trie = pickle.load(open(os.path.join(APP_STATIC, "airport_iata_trie.p"), "rb" ) )
airport_icao_trie = pickle.load(open(os.path.join(APP_STATIC, "airport_icao_trie.p"), "rb" ) )

airport_names_dictionary = pickle.load(open(os.path.join(APP_STATIC, "airport_names_dictionary.p"), "rb" ) )
airport_iata_dictionary = pickle.load(open(os.path.join(APP_STATIC, "airport_iata_dictionary.p"), "rb" ) )
airport_icao_dictionary = pickle.load(open(os.path.join(APP_STATIC, "airport_icao_dictionary.p"), "rb" ) )


@app.route('/')
def hello_world():
    return 'Site reached'


def get_exchange_rates(base_currency_code):
    base_url = 'http://api.fixer.io/latest'
    params = '?base={}'.format(base_currency_code)

    r = requests.get(base_url + params)

    if r.status_code == 200:
        return r.json()['rates']
    else:
        return None


@app.route('/autosuggest')
@cross_origin()
def search():
    term = request.args.get('q')
    if term is None or len(term) == 0:
        return Response({'error' : 'invalid query'}, mimetype='application/json', status=400)

    term = unicode(term).lower()

    name_matches = airport_name_trie.keys(term)
    iata_matches = airport_iata_trie.keys(term)
    icao_matches = airport_icao_trie.keys(term)

    airports = []
    icao_codes = set()

    for match in name_matches:
        airport = airport_names_dictionary[match]
        if airport.icao not in icao_codes:
            airports.append(airport)
            icao_codes.add(airport.icao)

    for match in iata_matches:
        airport = airport_iata_dictionary[match]
        if airport.icao not in icao_codes:
            airports.append(airport)
            icao_codes.add(airport.icao)

    for match in icao_matches:
        airport = airport_icao_dictionary[match]
        if airport.icao not in icao_codes:
            airports.append(airport)
            icao_codes.add(airport.icao)


    def getItem(x):
        return x.value(term)

    sorted_airports = sorted(airports, key=getItem, reverse=True)

    display_airports = []
    i = 0
    for a in sorted_airports:
        display_airports.append(u'{} ({})'.format(a.original_name, a.original_iata))
        i += 1
        if i >= MAX_SUGGESTIONS:
            break

    return Response(json.dumps(display_airports), mimetype='application/json')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
