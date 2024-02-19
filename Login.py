import base64
import hmac
import struct
import time

import data
import self
# from fyers_apiv import accessToken
from fyers_apiv3 import fyersModel
from pip._vendor import requests
from urllib.parse import urlparse, parse_qs

from totp import generate_token


class Login:
    def __init__(self) -> None:
        self.client_id = 'G66M7CCFRF-100'
        self.redirect_url = 'https://www.google.com/'
        self.response_type = 'code'
        self.state = 'state'
        self.secret_key = 'AUCC8730C1'
        self.grant_type = 'authorization_code'
        self.totp_key = 'ZERZ2G7MY2ZHG7SA24BQKGUHF5HOZNLW'
        self.username = 'XN19412'
        self.pin = '1010'
        self.access_token = None
        self.target1 = None
        self.target2 = None
        self.stop_loss1 = None
        self.stop_loss2 = None
        self.symbol = None
        self.quantity = None
        self.limitPrice = None
        self.productType = "INTRADAY"

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

    def totp(self, key, time_step=30, digits=6, digest="sha1"):
        key = base64.b32decode(key.upper() + "=" * ((8 - len(key)) % 8))
        counter = struct.pack(">Q", int(time.time() / time_step))
        mac = hmac.new(key, counter, digest).digest()
        offset = mac[-1] & 0x0F
        binary = struct.unpack(">L", mac[offset: offset + 4])[0] & 0x7FFFFFFF
        return str(binary)[-digits:].zfill(digits)

    def generate_token(self, refresh=False):
        if self.access_token == None and refresh != False:
            return
        headers = {
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        }

        s = requests.Session()
        s.headers.update(headers)

        data1 = f'{{"fy_id":"{base64.b64encode(f"{self.username}".encode()).decode()}","app_id":"2"}}'
        r1 = s.post("https://api-t2.fyers.in/vagator/v2/send_login_otp_v2", data=data1)
        assert r1.status_code == 200, f"Error in r1:\n {r1.json()}"

        request_key = r1.json()["request_key"]
        # print('request_key',request_key)
        data2 = f'{{"request_key":"{request_key}","otp":{self.totp(self.totp_key)}}}'
        r2 = s.post("https://api-t2.fyers.in/vagator/v2/verify_otp", data=data2)
        assert r2.status_code == 200, f"Error in r2:\n {r2.text}"

        request_key = r2.json()["request_key"]
        # print('request_key', request_key)
        data3 = f'{{"request_key":"{request_key}","identity_type":"pin","identifier":"{base64.b64encode(f"{self.pin}".encode()).decode()}"}}'
        r3 = s.post("https://api-t2.fyers.in/vagator/v2/verify_pin_v2", data=data3)
        assert r3.status_code == 200, f"Error in r3:\n {r3.json()}"

        headers = {"authorization": f"Bearer {r3.json()['data']['access_token']}",
                   "content-type": "application/json; charset=UTF-8"}
        data4 = f'{{"fyers_id":"{self.username}","app_id":"{self.client_id[:-4]}","redirect_uri":"{self.redirect_url}","appType":"100","code_challenge":"","state":"abcdefg","scope":"","nonce":"","response_type":"code","create_cookie":true}}'
        r4 = s.post("https://api.fyers.in/api/v2/token", headers=headers, data=data4)
        assert r4.status_code == 308, f"Error in r4:\n {r4.json()}"

        parsed = urlparse(r4.json()["Url"])
        auth_code = parse_qs(parsed.query)["auth_code"][0]

        session = fyersModel.SessionModel(client_id=self.client_id, secret_key=self.secret_key,
                                          redirect_uri=self.redirect_url, response_type="code",
                                          grant_type="authorization_code")
        session.set_token(auth_code)
        response = session.generate_token()
        self.access_token = response["access_token"]
        return self.access_token

    def get_profile(self):
        app.generate_token()
        fyers = fyersModel.FyersModel(client_id=self.client_id, token=self.access_token, log_path="")
        return fyers.get_profile()

    def placeorderfyer(self):
        #app.generate_token()
        fyers = fyersModel.FyersModel(client_id=self.client_id, token=self.access_token, log_path="")
        print('fyers', fyers.client_id, fyers.token)
        symbol = "NSE:SBIN-EQ"
        qty = 1
        type2 = 2
        side = 1
        data1 = {
            "symbol": symbol,
            "qty": qty,
            "type": type2,
            "side": side,
            "productType": "INTRADAY",

            "validity": "DAY",
            "disclosedQty": 0,
            "offlineOrder": "False",
            "stopLoss": 0,
            "takeProfit": 0
        }
        response = fyers.place_order(data1)
        print('response', response)


if __name__ == '__main__':
    app = Login()
    print(app.generate_token())
    print(app.get_profile())
    print(app.placeorderfyer())
