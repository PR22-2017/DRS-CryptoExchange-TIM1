from flask import Flask
import requests
app = Flask(__name__)


@app.route("/")
def main():
    api_link = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd'
    response = requests.get(api_link)
    data = response.json()
    ret_val = '<table class="table">'
    for value in data:
        ret_val += '<tr>'
        ret_val += '<td>'
        ret_val += value['name']
        ret_val += '</td>'
        ret_val += '<td>'
        ret_val += str(value['current_price'])
        ret_val += '</td>'
        ret_val += '</tr>'
    ret_val += '</table>'
    return ret_val


if __name__ == "__main__":
    app.run()
