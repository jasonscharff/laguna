class Airport():

    unknown_popularity_coefficient = 5000000.0

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






