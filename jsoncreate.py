import json
import os
import traceback

config = {'username': '', 'client_id': '', 'redirect_url': '', 'secret_key': '', 'totp_key': '',
          'pin': '',
          'access_token': '', 'target1': '', 'stop_loss1': '', 'quantity1': '', 'limitPrice1': '',
          'target2': '', 'stop_loss2': '', 'quantity2': '', 'limitPrice2': '', 'symbol': '','productType':''
          }


class jsoncreate:
    def __init__(self) -> None:
        global config
        try:
            if not os.path.exists('config1.json'):
                self.create_config_file()


        except:
            print(traceback.print_exc())
            config = json.load(open('config1.json'))
            print(config)
        self.client_id = config['client_id']
        self.redirect_url = config['redirect_url']
        self.response_type = 'code'
        self.state = 'state'
        self.secret_key = config['secret_key']
        self.grant_type = 'authorization_code'
        self.totp_key = config['totp_key']
        self.username = config['username']
        self.pin = config['pin']
        self.access_token = None
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
        self.config = config
        self.model = None
        if self.username == '' or self.client_id == '' or self.secret_key == '' or self.totp_key == '' or self.redirect_url == '' or self.target1 == '' or  self.target2=='' or self.stop_loss1=='' or self.stop_loss2=='' or self.quantity1=='' or self.quantity2=='':
            print('please enter all the details in the config.json file')
            exit()

    def create_config_file(self):
        file = json.dumps(config, indent=4)
        with open("../config1.json", "w") as f:
            f.write(file)
            f.close()


if __name__ == '__main__':
    dataconfig = jsoncreate()

    print(dataconfig.create_config_file())
