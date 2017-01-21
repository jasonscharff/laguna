from flask import Flask
import requests

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


def get_exchange_rates(currency_code):
    base_url = 'http://api.fixer.io/latest'
    params = '?base={}'.format(currency_code)
    r = requests.get(base_url + params)
    if r.status_code == 200:
        return r.json()['rates']
    else:
        return None




if __name__ == '__main__':
    app.run()
