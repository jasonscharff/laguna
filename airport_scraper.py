from bs4 import BeautifulSoup
import requests
import json



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





get_all_airports()






