import json, traceback
import os.path
import time
from fyers_api import fyersModel
# from fyers_apiv3 import fyersModel
from utils import Constant
from utils.Fyers_Utilty import Fyers_Utilty

config = {'target1': '', 'stop_loss1': '', 'quantity1': '', 'limitPrice1': '',
          'symbol': '', 'stop_loss_percent': ''
          }


class Nifty_Buy_CE_Option:
    def __init__(self) -> None:
        global config
        try:
            if not os.path.join(os.getcwd().join(Constant.NIFTY_BUY_CE_OPTION.strip())):
                self.create_config_file()
                print("file not exists", os.getcwd())
            else:
                print("file  exist", os.getcwd())
        except:
            print(traceback.print_exc())
        config = json.load(open(Constant.NIFTY_BUY_CE_OPTION))
        print('Buy_config--', config)
        self.target1 = config['target1']
        self.limitPrice1 = config['limitPrice1']
        self.symbol = config['symbol']
        self.quantity1 = config['quantity1']
        self.stop_loss_percent = config['stop_loss_percent']
        self.config = config
        self.model = None
        if self.target1 == '' or self.quantity1 == '' or self.stop_loss_percent == '':
            print(self.target1, 'self.target1',
                  'self.quantity1-', self.quantity1)
            print('please enter all the details in the Nifty_Buy_CE_Option.json file')
            exit()

    def create_config_file(self):
        file = json.dumps(config, indent=10)
        with open("../../config/Nifty_Buy_CE_Option.json", "w") as f:
            f.write(file)
            f.close()

    def place_order_1(self):
        global counter, Buy_FinalSL
        fyerUtils = Fyers_Utilty()
        classname = dataconfig.__class__.__name__
        print('classname', classname)
        fyers = fyersModel.FyersModel(client_id=fyerUtils.client_id, token=fyerUtils.access_token, log_path="")
        fyerUtils = Fyers_Utilty()
        side = 1
        intrade = 1
        productType = Constant.PRODUCT_TYPE
        self.symbol = fyerUtils.get_CE_FNO_Data(classname)
        symbol2 = {"symbols": self.symbol}
        filterStockPrice = dataconfig.get_LTP(symbol2)
        data1 = {
            "symbol": self.symbol,
            "qty": self.quantity1,
            "type": 1,
            "side": side,
            "productType": Constant.PRODUCT_TYPE,
            "limitPrice": filterStockPrice,
            "stopPrice": 0,
            "validity": "DAY",
            "disclosedQty": 0,
            "offlineOrder": "False",
            "stopLoss": 0,
            "takeProfit": self.target1
        }
        try:

            while True:
                self.config['symbol'] = self.symbol
                self.limitPrice1 = filterStockPrice
                self.config['limitPrice1'] = self.limitPrice1
                with open(Constant.NIFTY_BUY_CE_OPTION, 'w') as f:
                    f.write(json.dumps(self.config))
                    f.close()
                config4 = json.load(open(Constant.NIFTY_BUY_CE_OPTION))
                print('\033[93m-------------------------place_order 1---------------------------')
                print('Order still not placed in Sell place_order 1 for ', self.symbol, 'with LTP -', filterStockPrice,
                      ' and with LIMIT Price1 - ',
                      config4['limitPrice1'])
                print('current time--', time.strftime(" %H:%M:%S"))
                if Constant.PAPER_TRADE == 'YES':
                    print('You are trading with PaperWork')
                else:
                    response = fyers.place_order(data1)
                    print('Order Placed  in place_order 1 with LTP ', filterStockPrice, response)
                break
            Buy_FinalSL = 50
            while intrade == 1:
                symbol2 = {"symbols": self.symbol}
                ltp = dataconfig.get_LTP(symbol2)
                print('current time--', time.strftime('%H:%M:%S'))
                print('ltp in first while loop ', ltp)
                config1 = json.load(open(Constant.NIFTY_BUY_CE_OPTION))
                entry_price = config1['limitPrice1']
                stop_loss_percent = config1['stop_loss_percent']
                current_price = ltp
                Buy_trailing_stop_loss_price = fyerUtils.Buy_trailing_stop_loss(current_price,
                                                                                int(entry_price),
                                                                                int(stop_loss_percent))
                # print('Buy_FinalSL1111--', int(Buy_FinalSL))
                # print('Buy_trailing_stop_loss_price1111--', int(Buy_trailing_stop_loss_price))
                time.sleep(1)
                ExitId = {"id": "" + (self.symbol + '-' + productType) + ''}
                if time.strftime('%H:%M') == Constant.TRADE_SQUARE_OFF:
                    fyerUtils.exit_position(ExitId)
                    print('Trade is Squared OFF')
                    return
                print('-----------------------Machine - 1--Buying CE mode---------------------------')
                print('Buy stop_loss1', int(Buy_FinalSL))

                Target = int(config1['limitPrice1']) + int(config1['target1'])
                print('Buy target1', Target)
                if Buy_trailing_stop_loss_price > Buy_FinalSL:
                    Buy_FinalSL = Buy_trailing_stop_loss_price
                if (side == 1) and (ltp is not None and ltp <= Buy_FinalSL):
                    self.config['symbol'] = None
                    self.config['limitPrice1'] = 0
                    with open(Constant.NIFTY_BUY_CE_OPTION, 'w') as f:
                        f.write(json.dumps(self.config))
                        f.close()
                    print("Stop loss hit for " + self.symbol + ' at ' + str(ltp))
                    # ExitId = {"id": "NSE:AARTIIND-EQ-INTRADAY"}
                    print('exit data', ExitId)
                    fyerUtils.exit_position(ExitId)
                    return

                elif (side == 1) and (ltp is not None and ltp >= Target):
                    fyerUtils.exit_position(ExitId)
                    print("Profit booked in First Go for " + self.symbol + ' at ' + str(ltp))
                    return
                else:
                    time.sleep(1)
        except:
            print(traceback.print_exc())

    def get_LTP(self, symbol):
        fyerUtils = Fyers_Utilty()
        try:
            fyers = fyersModel.FyersModel(client_id=fyerUtils.client_id, token=fyerUtils.access_token, log_path="")
            ltp = fyers.quotes(symbol)['d'][0]['v']['lp']
            print('LTP of ', self.symbol, ' is ', ltp)
            return ltp
        except:
            print(traceback.print_stack())


if __name__ == '__main__':
    dataconfig = Nifty_Buy_CE_Option()
    dataconfig.place_order_1()
    flag = True
    while flag:
        if time.strftime('%H:%M') == '09:29':
            dataconfig.place_order_1()
            flag = False
