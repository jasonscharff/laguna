class Airport():

    unknown_popularity_coefficient = 10

    def __init__(self, airport_json, popularity_coefficient=unknown_popularity_coefficient):

        self.popularity_coefficient = popularity_coefficient
        self.iata = airport_json['iata']
        self.icao = airport_json['icao']
        self.name = airport_json['airport_name']
        self.location = airport_json['location_served']

    #very simple, super arbitrary valuation.
    def value(self, search_term):
        airport_sum = 0

        if (self.iata.startswith(search_term)):
            airport_sum += 25
        if (self.icao.startswith(search_term)):
            airport_sum += 20
        if (self.name.startswith(search_term)):
            airport_sum += 15
        if airport_sum > 0:
            airport_sum += self.popularity_coefficient

        return airport_sum


