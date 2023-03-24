from flask import Flask, request
import json
import ccxt

exchange = ccxt.bitget({
    # Free to get the api key from your exchange
    'apiKey': "",
    'secret': "",
    # bitget requires password as addition info to login. Good to remove for the other exchanges
    'password':"",
    "enableRateLimit": False,
    })


# short open short order
# Tss stop sell the short order

# long open long order
# Tsl sell the long order


def orderHandler(data):
    # Adjust this number to change the leverage, e.g 1-100,min is 1, the max is 125 dependes on the crypto
    exchange.set_leverage(100, data["symbol"])

    side = None

    if data["openSide"] == "short":
        side = "open_short"
    if data["openSide"] == "long":
        side = "open_long"
    if data["openSide"] == "Tsl":
        side = "close_long"
    if data["openSide"] == "Tss":
        side = "close_short"

    exchange.private_mix_post_order_placeorder({
        "symbol": data["symbol"],
        # I only do ETH/USDT so marginCoin will be USDT.
        "marginCoin": "USDT",
        # size means how many crypto you want to buy
        # For ETH the min is 0.03. The min size is different for every crypto
        "size": "0.03",
        "side":side,
        # market price or "limit",if limit then need to add one more param which is --cant remember
        "orderType":"market"
    })


def requestDataHandler(data):
    code = {
        # Since Tradingview returns ETHUSDT.P (swap) so need to convert it to a code that Bybit knows
        "ETHUSDT.P": "ETHUSDT_UMCBL"
    }
    # "symbol" "asx" are all the params sent from tradingView. You will need to adjust this part
    symbol = code[data["symbol"]]
    openSide = data["asx"]

    return {"symbol":symbol,"openSide":openSide}

app = Flask(__name__)
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
app.after_request(after_request)

@app.route("/open",methods=['POST'])
def open1():
    _data = json.loads(request.data)
    data = requestDataHandler(_data)
    orderHandler(data)
    return '1'

if __name__ == '__main__':
    app.run('0.0.0.0', 80)



