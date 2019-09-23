# coding: utf-8
import json, hmac, hashlib, time, requests
import config as Config
import sys, os
from requests.auth import AuthBase
from flask import jsonify, request

reload(sys)
sys.setdefaultencoding('utf8')
app = Config.config()
# Before implementation, set environmental variables with the names API_KEY and API_SECRET
API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']
# Create custom authentication for Coinbase API
class CoinbaseWalletAuth(AuthBase):
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key

    def __call__(self, request):
        timestamp = str(int(time.time()))
        message = timestamp + request.method + request.path_url + (request.body or '')
        signature = hmac.new(self.secret_key, message, hashlib.sha256).hexdigest()
        request.headers.update({
            'CB-ACCESS-SIGN': signature,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
        })
        return request

api_url = 'https://api.coinbase.com/v2/'
auth = CoinbaseWalletAuth(API_KEY, API_SECRET)

class Wallet():
    total_wallet = {}
    list_jeton = []
    def __init__(self):
        print("Init Wallet class")
        r = requests.get(api_url + 'accounts', auth=auth)
        rjson = r.json()
        List = []
        total_wallet = {}
        total_wallet["spot_wallet"] = 0
        total_wallet["sell_wallet"] = 0
        for x in range(len(rjson["data"])):
            data_jeton = {}
            name_jeton = rjson["data"][x]["balance"]["currency"]
            data_jeton["name_jeton"] = name_jeton
            if (name_jeton == "EUR" or name_jeton == "USDC"):
                continue

            #Quantité de jeton
            nbr_jetons = rjson["data"][x]["balance"]["amount"]
            data_jeton["nbr_jetons"] = nbr_jetons

            #Prix actuelle d'un jeton
            r = requests.get(api_url + 'prices/' + name_jeton + '-EUR/spot', auth=auth)
            value_spot_jeton = r.json()["data"]["amount"]
            data_jeton["spot_jeton"] = value_spot_jeton

            #Prix d'achat d'un jeton
            r = requests.get(api_url + 'prices/' + name_jeton + '-EUR/buy', auth=auth)
            value_buy_jeton = r.json()["data"]["amount"]
            data_jeton["buy_jeton"] = value_buy_jeton

            #Prix de vente d'un jeton
            r = requests.get(api_url + 'prices/' + name_jeton + '-EUR/sell', auth=auth)
            value_sell_jeton = r.json()["data"]["amount"]
            data_jeton["sell_jeton"] = value_sell_jeton

            #Prix actuelle de tous les jetons
            data_jeton["spot_wallet_jeton"] = float(value_spot_jeton) * float(nbr_jetons)
            total_wallet["spot_wallet"] += data_jeton["spot_wallet_jeton"]

            #Prix de vente de tous les jetons
            data_jeton["sell_wallet_jeton"] = float(value_sell_jeton) * float(nbr_jetons)
            total_wallet["sell_wallet"] += data_jeton["sell_wallet_jeton"]
            List.append(data_jeton)
        self.total_wallet = total_wallet
        self.list_jeton = List

    def setWallet(self, wallet, jeton):
        self.total_wallet = wallet
        self.list_jeton = jeton
    def getWallet(self):
        return self.total_wallet
    def getJeton(self):
        return self.list_jeton


@app.route('/')
def home():
    try:
        index_jeton = int(request.args.get('index'))
        MyWallet = Wallet()
        listjeton = MyWallet.getJeton()
        print(len(listjeton))
        jeton_display = []
        jeton_display.append(listjeton[index_jeton])
        jeton_display.append(listjeton[index_jeton + 1])
        jeton_display.append(listjeton[index_jeton + 2])
        return jsonify(
            jeton = listjeton,
#           wallet = MyWallet.getWallet()
        )
    except IndexError:
        return jsonify(
            error = "Index is too big max integer is " + str(len(listjeton)- 3)
        )
    except Exception:
        return jsonify(
            error = "Please enter a query index=integer"
        )

#Example http://127.0.0.1:5000/test?jeton=XLM
@app.route('/test')
def test():
    name_jeton = request.args.get('jeton')

    r = requests.get(api_url + 'prices/' + name_jeton + '-EUR/spot', auth=auth)
    spot = r.json()["data"]["amount"]

    r = requests.get(api_url + 'prices/' + name_jeton + '-EUR/buy', auth=auth)
    buy = r.json()["data"]["amount"]

    r = requests.get(api_url + 'prices/' + name_jeton + '-EUR/sell', auth=auth)
    sell = r.json()["data"]["amount"]
    return jsonify(
        spot = spot,
        buy = buy,
        sell = sell
    )