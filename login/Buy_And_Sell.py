import base64
import hmac
import json, traceback
import os.path
import struct
import time

import data
import self
from fyers_api import accessToken
from fyers_api import fyersModel
from pip._vendor import requests
from urllib.parse import urlparse, parse_qs

config = {'username': '', 'client_id': '', 'redirect_url': '', 'secret_key': '', 'totp_key': '',
          'pin': '',
          'access_token': '', 'target1': '', 'stop_loss1': '', 'quantity1': '', 'limitPrice1': '',
          'target2': '', 'stop_loss2': '', 'quantity2': '', 'limitPrice2': '', 'symbol': '', 'productType': '',
          'token generated_on': ''
          }


class Buy_Order:
    def __init__(self) -> None:
        global config
        try:
            print('CWD--',os.path.join(os.getcwd()))
            if not os.path.join(os.getcwd().join('/config/Buy_config.json'.strip())):
                self.create_config_file()
                print("file not exists", os.getcwd())
            else:
                print("file  exist", os.getcwd())


        except:
            print(traceback.print_exc())
        config = json.load(open('Buy_config.json'))
        print('config--', config)
        self.client_id = config['client_id']
        self.redirect_url = config['redirect_url']
        print('redirect_url in config', config['redirect_url'])
        self.response_type = 'code'
        self.state = 'state'
        self.secret_key = config['secret_key']
        self.grant_type = 'authorization_code'
        self.totp_key = config['totp_key']
        self.username = config['username']
        self.pin = config['pin']
        self.access_token = config['access_token']
        self.target1 = config['target1']
        self.target2 = config['target2']
        self.stop_loss1 = config['stop_loss1']
        self.stop_loss2 = config['stop_loss2']
        self.symbol = config['symbol']
        self.quantity1 = config['quantity1']
        self.quantity2 = config['quantity2']
        self.limitPrice1 = config['limitPrice1']
        self.limitPrice2 = config['limitPrice2']
        self.productType = config['productType']
        self.token_generated_on = config['token generated_on']
        self.config = config
        self.model = None
        if self.username == '' or self.client_id == '' or self.secret_key == '' or self.totp_key == '' or self.redirect_url == '' or self.target1 == '' or self.target2 == '' or self.stop_loss1 == '' or self.stop_loss2 == '' or self.quantity1 == '' or self.quantity2 == '':
            print('self.username-', self.username, self.client_id, self.secret_key, self.totp_key, self.redirect_url,
                  self.target1, 'elf.target2-', self.target2, 'self.stop_loss1-', self.stop_loss1, 'self.stop_loss2-',
                  self.stop_loss2, 'self.quantity1-', self.quantity1, 'self.quantity2', self.quantity2)
            print('please enter all the details in the Buy_config.json file')
            exit()

    def create_config_file(self):
        file = json.dumps(config, indent=10)
        with open("../Buy_config.json", "w") as f:
            f.write(file)
            f.close()

    def enable_app(self):
        appSession = accessToken.SessionModel(
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
        # print('self.access_token----',self.access_token)
        if len(self.access_token) > 10 and refresh == False:
            # print('self.access_token in generate_token()', self.access_token)
            if int(self.token_generated_on) >= int(time.time()):
                return
        headers = {
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/112.0.0.0 Safari/537.36",
        }
        try:
            s = requests.Session()
            s.headers.update(headers)

            data1 = f'{{"fy_id":"{base64.b64encode(f"{self.username}".encode()).decode()}","app_id":"2"}}'
            r1 = s.post("https://api-t2.fyers.in/vagator/v2/send_login_otp_v2", data=data1)
            assert r1.status_code == 200, f"Error in r1:\n {r1.json()}"

            request_key = r1.json()["request_key"]

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

            session = accessToken.SessionModel(client_id=self.client_id, secret_key=self.secret_key,
                                               redirect_uri=self.redirect_url, response_type="code",
                                               grant_type="authorization_code")
            print('session--', self.client_id, self.secret_key)
            session.set_token(auth_code)
            response = session.generate_token()
            self.access_token = response["access_token"]
            self.config['access_token'] = self.access_token
            self.config['token_generated_on'] = time.time()
            with open('Buy_config.json', 'w') as f:
                f.write(json.dumps(self.config))
                f.close()
            return self.access_token
        except:
            traceback.print_stack()

    def get_model(self):
        if self.model is None:
            self.generate_token()
            self.model = fyersModel.FyersModel(client_id=self.client_id, token=self.access_token,
                                               log_path="C:\\Users\\ADMIN\\Documents\\")
            return self.model

    def get_profile(self):
        try:
            print('self.generate_token() in get_profile', self.generate_token())
            return dataconfig.get_model().get_profile()
        except:
            print(traceback.print_exc())

    def place_order_1(self):

        side = 1
        intrade = 1
        symbol = {"symbols": self.symbol}
        ltp = 279.1 #dataconfig.get_LTP(symbol)
        data1 = {
            "symbol": self.symbol,
            "qty": self.quantity1,
            "type": 1,
            "side": side,
            "productType": self.productType,
            "limitPrice": self.limitPrice1,
            "stopPrice": 0,
            "validity": "DAY",
            "disclosedQty": 0,
            "offlineOrder": "False",
            "stopLoss": self.stop_loss1,
            "takeProfit": self.target1
        }
        try:

            response = self.get_model().place_order(data1)
            print('response in place_order 1 ',response)
        except:
            print(traceback.print_exc())

        while intrade == 1:
            ltp = dataconfig.get_LTP(symbol)
            print('ltp in first while loop ', ltp)
            time.sleep(3)
            counter_one=0
            print('count',counter_one)
            ExitId = {"id": "" + (self.symbol + '-' + self.productType) + ''}
            if ((side == 1) and (str(ltp) <= self.stop_loss1)) or ((dir == "SELL") and (str(ltp) >= self.stop_loss1)):
                print("Stop loss hit first time of " + self.symbol + ' at ' + str(ltp))
                # ExitId = {"id": "NSE:AARTIIND-EQ-INTRADAY"}
                print('exit data', ExitId)
                dataconfig.exit_position(ExitId)
                dataconfig.place_order_2()
                intrade = 0
                while intrade == 0:
                    ltp = dataconfig.get_LTP(symbol)
                    print('ltp in second while loop ', ltp)
                    time.sleep(3)
                    count=1
                    print('count',count+1)
                    ExitId = {"id": "" + (self.symbol + '-' + self.productType) + ''}
                if ((side == 1) and (str(ltp) <= self.stop_loss2)) or ((dir == "SELL") and (str(ltp) >= self.stop_loss2)):

                    # ExitId = {"id": "NSE:AARTIIND-EQ-INTRADAY"}
                    print('exit data', ExitId)
                    dataconfig.exit_position(ExitId)
                    print("Stop loss hit second time of " + self.symbol + ' at ' + str(ltp))
                    intrade = 2
                    return
                elif ((side == 1) and (str(ltp) >= self.target2)) or ((dir == "SELL") and (str(ltp) <= self.target2)):
                      dataconfig.exit_position(ExitId)
                      print("Profit booked for " + self.symbol + ' at ' + str(ltp))
                      return

            elif ((side == 1) and (str(ltp) >= self.target1)) or ((dir == "SELL") and (str(ltp) <= self.target1)):
                print('ltp price in profit booking', ltp)
                dataconfig.exit_position(ExitId)
                print("Profit booked for " + self.symbol + ' at ' + str(ltp))
                return
            else:
                time.sleep(1)



    def get_LTP(self, symbol):
        try:
            fyers = fyersModel.FyersModel(client_id=self.client_id, token=self.access_token, log_path="")
            ltp = fyers.quotes(symbol)['d'][0]['v']['lp']
            print('ltp of', ltp)
            return ltp
        except:
            print(traceback.print_stack())

    def exit_position(self, exitid):
        try:
            fyers = fyersModel.FyersModel(client_id=self.client_id, token=self.access_token, log_path="")
            response = fyers.exit_positions(exitid)
            print(response)
            return response
        except:
            print(traceback.print_stack())

    def place_order_2(self):
        side = 1
        data2 = {
            "symbol": self.symbol,
            "qty": self.quantity2,
            "type": 1,
            "side": side,
            "productType": self.productType,
            "limitPrice": self.limitPrice2,
            "stopPrice": 0,
            "validity": "DAY",
            "disclosedQty": 0,
            "offlineOrder": "False",
            "stopLoss": self.stop_loss2,
            "takeProfit": self.target2
        }

        try:
            fyers = fyersModel.FyersModel(client_id=self.client_id, token=self.access_token, log_path="")
            response = fyers.place_order(data2)
            print('response in place_order 2 ', response)
        except:
            print(traceback.print_exc())


if __name__ == '__main__':
    dataconfig = Buy_Order()
    dataconfig.place_order_1()
    # dataconfig.generate_token()
