import time

from fyers_apiv3 import fyersModel
import Login

class LoginSample:
    global tradeCount

    def __init__(self) -> None:
        self.client_id = 'G66M7CCFRF-100'
        self.redirect_url = 'https://www.google.com/'
        self.response_type = 'code'
        self.state = 'state'
        self.secret_key = 'AUCC8730C1'
        self.grant_type = 'authorization_code'
        self.totp_key = 'YWJXSUK24GMUFCCD327EJ3PXO2EVNDMX'
        self.username = 'XN19412'
        self.pin = '1010'
        self.access_token = None

    def enable_app(self):
        appSession = fyersModel.SessionModel(
            client_id=self.client_id,
            secret_key=self.secret_key,
            redirect_uri=self.redirect_url,
            response_type='code',
            state='state',
            grant_type='authorization_code'
        )
        return appSession.generate_authcode()

    def placeOrderFyers(self, symbol, t_type, qty, order_type):

        global oidexit
        Login.generate_token()
        fyers = fyersModel.FyersModel(client_id=self.client_id, token=self.access_token, log_path="")

    Trade1_target_price = 1300
    Trade1_stoploss_price = 1200
    Trade2_stoploss_price = Trade1_stoploss_price - 10
    Trade2_target_price = Trade1_target_price
    symbol = "NSE:INFY-EQ"
    dir = "BUY"
    intrade = 1
    qty = 5
    ltp = 1200
    tradeCount = 0

    while intrade == 1:

        if (dir == "BUY") and (ltp <= Trade1_stoploss_price):
            oidexit = placeOrderFyers(symbol, "SELL", qty, "MARKET", 0)
            ltp = Trade1_stoploss_price
            print("stop loss hit: ", ltp)
            intrade = 0
            tradeCount = 1
            break
        elif (dir == "SELL") and (ltp <= Trade1_stoploss_price):
            oidexit = placeOrderFyers(symbol, "BUY", qty, "MARKET", 0)
            print("stop loss hit: ", oidexit)
            intrade = 0
        elif ((dir == "SELL") and (ltp <= Trade1_target_price) or (ltp >= Trade1_stoploss_price)):
            oidexit = placeOrderFyers(symbol, "BUY", qty, "MARKET", 0)
            print("Order Exited: ", oidexit)
        intrade = 0
    else:
        time.sleep(1)

    while intrade == 0 and tradeCount == 1:
        app.placeOrder2Fyers("NSE:INFY-EQ", ltp, 10, "MARKET", Trade2_stoploss_price, Trade2_target_price)

        data = {
            "symbol": "NSE:SBIN-EQ",
            "qty": 1,
            "type": 2,
            "side": 1,
            "productType": "INTRADAY",
            "limitPrice": 0,
            "stopPrice": 0,
            "validity": "DAY",
            "disclosedQty": 0,
            "offlineOrder": "False",
        }
    print('data', data)

    def placeOrder2Fyers(self, symbol, limitPrice, qty, order_type, stoploss_price, target_price):

        fyers1 = fyersModel.FyersModel(client_id=self.client_id, token=self.access_token, log_path="")
        if tradeCount == 1:
            tradeorder = fyers1
            return tradeorder


if __name__ == '__main__':
    app = LoginSample()
    app.placeOrder2Fyers()

    print(app.placeOrderFyers("NSE:INFY-EQ", 2, 10, "MARKET"))
