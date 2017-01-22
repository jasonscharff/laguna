class Airport():

    unknown_popularity_coefficient = 10000000.0

    def __init__(self, airport_json, popularity=unknown_popularity_coefficient):
        self.popularity_coefficient = popularity

        self.original_iata = unicode(airport_json['iata'])
        self.iata = self.original_iata.lower()
        self.icao = unicode(airport_json['icao']).lower()
        self.original_name = unicode(airport_json['airport_name'])
        self.name = self.original_name.lower()
        self.location = unicode(airport_json['location_served']).lower()

    #very simple, super arbitrary valuation.
    def value(self, search_term):
        airport_sum = 0.0

        if (self.iata.startswith(search_term)):
            airport_sum += 25.0
        elif (self.icao.startswith(search_term)):
            airport_sum += 20.0
        elif (self.name.startswith(search_term)):
            airport_sum += 15.0
        if airport_sum > 0:
            val = float(self.popularity_coefficient)
            divisor = 1000000.0
            popularity_factor = val/divisor
            airport_sum += popularity_factor

        return airport_sum



import pickle
import marisa_trie


airport_name_trie = pickle.load( open( "serialized/airport_names_trie.p", "rb" ) )
airport_iata_trie = pickle.load( open( "serialized/airport_iata_trie.p", "rb" ) )
airport_icao_trie = pickle.load( open( "serialized/airport_icao_trie.p", "rb" ) )

airport_names_dictionary = pickle.load( open( "serialized/airport_names_dictionary.p", "rb"))
airport_iata_dictionary = pickle.load( open( "serialized/airport_iata_dictionary.p", "rb" ))
airport_icao_dictionary = pickle.load( open( "serialized/airport_icao_dictionary.p", "rb" ))



def search(term):
    term = term.lower()
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
    for i in sorted_airports:
         print i.iata



search(u'San franc')




