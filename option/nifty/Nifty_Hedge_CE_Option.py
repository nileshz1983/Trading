import json, traceback
import os.path
import time
from fyers_api import fyersModel
from utils import Constant
from utils.Fyers_Utilty import Fyers_Utilty

config = {'target1': '', 'stop_loss1': '', 'quantity1': '', 'limitPrice1': '',
          'target2': '', 'stop_loss2': '', 'quantity2': '', 'limitPrice2': '', 'symbol': '', 'productType': '',
          'stop_loss_percent': '', 'Premium_Price': ''
          }


class Nifty_Hedge_PE_Option:
    def __init__(self) -> None:
        global config
        try:
            if not os.path.join(os.getcwd().join(Constant.NIFTY_HEDGE_PE_OPTION.strip())):
                self.create_config_file()
                print("file not exists", os.getcwd())
            else:
                print("file  exist", os.getcwd())
        except:
            print(traceback.print_exc())
        config = json.load(open(Constant.NIFTY_HEDGE_PE_OPTION))
        print('Buy_config--', config)
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
        self.stop_loss_percent = config['stop_loss_percent']
        self.Premium_Price = config['Premium_Price']
        self.config = config
        self.model = None
        if self.target1 == '' or self.target2 == '' or self.stop_loss1 == '' or self.stop_loss2 == '' or self.quantity1 == '' or self.quantity2 == '' or self.stop_loss_percent == '' or self.Premium_Price == '':
            print(self.target1, 'elf.target2-', self.target2, 'self.stop_loss1-', self.stop_loss1, 'self.stop_loss2-',
                  self.stop_loss2, 'self.quantity1-', self.quantity1, 'self.quantity2', self.quantity2)
            print('please enter all the details in the Nifty_Buy_PE_Option.json file')
            exit()

    def create_config_file(self):
        file = json.dumps(config, indent=10)
        with open("../../config/Nifty_Buy_PE_Option.json", "w") as f:
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
        # symbol = {"symbols": self.symbol}

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

            while True:
                self.symbol = fyerUtils.get_PE_FNO_Data(classname)

                filterStock = self.symbol
                # print('self.symbol-------', self.symbol)
                symbol2 = {"symbols": self.symbol}
                # print('symbol2-------', symbol2)
                filterStockPrice = dataconfig.get_LTP(symbol2)
                print(filterStock, dataconfig.get_LTP(symbol2))
                self.config['symbol'] = self.symbol
                self.limitPrice1 = filterStockPrice
                self.config['limitPrice1'] = self.limitPrice1
                with open(Constant.NIFTY_HEDGE_PE_OPTION, 'w') as f:
                    f.write(json.dumps(self.config))
                    f.close()
                config4 = json.load(open(Constant.NIFTY_HEDGE_PE_OPTION))
                print('\033[92m-------------------------place_order 1---------------------------')
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
            Buy_FinalSL = 0
            while intrade == 1:
                symbol2 = {"symbols": self.symbol}
                ltp = dataconfig.get_LTP(symbol2)
                print('current time--', time.strftime('%H:%M:%S'))
                print('ltp in first while loop ', ltp)
                config1 = json.load(open(Constant.NIFTY_HEDGE_PE_OPTION))
                entry_price = config1['limitPrice1']
                stop_loss_percent = config1['stop_loss_percent']
                current_price = ltp
                Buy_trailing_stop_loss_price = fyerUtils.Buy_trailing_stop_loss(current_price,
                                                                                int(entry_price),
                                                                                int(stop_loss_percent))
                # print('Buy_FinalSL1111--', int(Buy_FinalSL))
                # print('Buy_trailing_stop_loss_price1111--', int(Buy_trailing_stop_loss_price))
                time.sleep(2)
                ExitId = {"id": "" + (self.symbol + '-' + self.productType) + ''}
                if time.strftime('%H:%M') == '15:13':
                    fyerUtils.exit_position(ExitId)
                    print('Trade is Squared OFF')
                    return
                print('-----------------------Machine - 2--Buying PE mode---------------------------')
                print('Buy stop_loss1', int(Buy_FinalSL))

                Target = int(config1['limitPrice1']) + int(config1['target1'])
                print('Buy target1', Target)
                if Buy_trailing_stop_loss_price > Buy_FinalSL:
                    Buy_FinalSL = Buy_trailing_stop_loss_price
                if (side == 1) and (ltp is not None and ltp <= Buy_FinalSL):
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
    dataconfig = Nifty_Hedge_PE_Option()
    dataconfig.place_order_1()
    flag = True
    while flag:
        if time.strftime('%H:%M') == '09:29':
            dataconfig.place_order_1()
            flag = False
