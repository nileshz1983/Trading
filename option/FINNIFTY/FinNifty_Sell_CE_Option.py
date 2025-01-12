import base64
import json, traceback
import os.path
import time
from fyers_api import fyersModel, accessToken
from utils import Constant
from utils.Fyers_Utilty import Fyers_Utilty
import sys

print('sys.path', sys.path)

config = {'target1': '', 'stop_loss1': '', 'quantity1': '', 'limitPrice1': '',
          'target2': '', 'stop_loss2': '', 'quantity2': '', 'limitPrice2': '', 'symbol': '', 'productType': '',
          'Premium_Price': '', 'stop_loss_1_percent': '', 'stop_loss_2_percent': '',
          'Order2_Execution_Flag': ''
          }


class FinNifty_Sell_PE_Option:

    def __init__(self) -> None:
        global config

        try:
            if not os.path.join(os.getcwd().join(Constant.FINNIFTY_SELL_PE_OPTION.strip())):
                self.create_config_file()
                print("file not exists", os.getcwd())
            else:
                print("file  exist", os.getcwd())
        except:
            print(traceback.print_exc())
        config = json.load(open(Constant.FINNIFTY_SELL_PE_OPTION))
        print("\033[93mSell_config--", config)
        self.target1 = config['target1']
        self.target2 = config['target2']
        self.stop_loss1 = config['stop_loss1']
        self.stop_loss2 = config['stop_loss2']
        self.symbol = config['symbol']
        self.quantity1 = config['quantity1']
        self.quantity2 = config['quantity2']
        self.limitPrice1 = config['limitPrice1']
        self.limitPrice2 = config['limitPrice2']
        self.Premium_Price = config['Premium_Price']
        self.productType = config['productType']
        self.Order2_Execution_Flag = config['Order2_Execution_Flag']
        self.stop_loss_1_percent = config['stop_loss_1_percent']
        self.stop_loss_2_percent = config['stop_loss_2_percent']
        self.config = config
        self.model = None
        if self.target1 == '' or self.target2 == '' or self.stop_loss1 == '' or self.stop_loss2 == '' or self.quantity1 == '' or self.quantity2 == '' or self.Premium_Price == '' or self.stop_loss_1_percent == '' or self.stop_loss_2_percent == '':
            print(self.target1, 'elf.target2-', self.target2, 'self.stop_loss1-', self.stop_loss1, 'self.stop_loss2-',
                  self.stop_loss2, 'self.quantity1-', self.quantity1, 'self.quantity2', self.quantity2)
            print('please enter all the details in the FINNIFTY_SELL_PE_OPTION.json file')
            exit()

    def create_config_file(self):
        file = json.dumps(config, indent=10)
        with open("../../config/FINNIFTY_SELL_PE_OPTION.json", "w") as f:
            f.write(file)
            f.close()

    def place_order_1(self):
        global counter, Sell_FinalSL, Buy_FinalSL, symbol2
        fyerUtils = Fyers_Utilty()
        classname = dataconfig.__class__.__name__

        fyers = fyersModel.FyersModel(client_id=fyerUtils.client_id, token=fyerUtils.access_token, log_path="")

        side = -1
        intrade = 1
        symbol = {"symbols": self.symbol}
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
            "offlineOrder": "False"
        }
        try:
            while True:
                self.symbol = fyerUtils.get_PE_FNO_Data(classname)
                print('symbol1-------', self.symbol)
                filterStock = self.symbol

                symbol2 = {"symbols": filterStock}
                filterStockPrice = dataconfig.get_LTP(symbol2)
                print(filterStock, dataconfig.get_LTP(symbol2))
                self.config['symbol'] = self.symbol
                self.limitPrice1 = filterStockPrice
                print('filterStockPrice---', filterStockPrice)
                self.config['limitPrice1'] = self.limitPrice1
                with open(Constant.FINNIFTY_SELL_PE_OPTION, 'w') as f:
                    f.write(json.dumps(self.config))
                    f.close()
                config4 = json.load(open(Constant.FINNIFTY_SELL_PE_OPTION))
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
                # print('Order Placed  in place_order 1 with LTP ', ltp)
                break
        except:
            print(traceback.print_exc())
        Sell_FinalSL = 1000.0
        fyerUtils = Fyers_Utilty()
        while intrade == 1:
            print('current time--', time.strftime('%H:%M:%S'))

            ltp = dataconfig.get_LTP(symbol2)
            time.sleep(2)
            config1 = json.load(open(Constant.FINNIFTY_SELL_PE_OPTION))
            entry_price = config1['limitPrice1']
            Order2_Execution_Flag = config1['Order2_Execution_Flag']
            print('Order2_Execution_Flag -- ', Order2_Execution_Flag)
            stop_loss_1_percent = config1['stop_loss_1_percent']
            current_price = ltp
            sell_trailing_stop_loss_price = fyerUtils.Sell_trailing_stop_loss(current_price, int(entry_price),
                                                                              int(stop_loss_1_percent))
            print('Sell_FinalSL111--', Sell_FinalSL)
            print('sell_trailing_stop_loss_price1111--', sell_trailing_stop_loss_price)
            ExitId = {"id": "" + (self.symbol + '-' + self.productType) + ''}
            if time.strftime('%H:%M') == Constant.TRADE_SQUARE_OFF:
                fyerUtils.exit_position(ExitId)
                print('Trade is Squared OFF')
                return
            print('\033[96m---------------------Machine2----Selling PE mode with Order 1 ---------------------------')
            print('Stop_loss1', Sell_FinalSL)
            Target1 = int(config1['limitPrice1']) - int(config1['target1'])
            print('Target1', Target1)
            # ltp = 368
            if sell_trailing_stop_loss_price < Sell_FinalSL:
                Sell_FinalSL = sell_trailing_stop_loss_price
            if (side == -1) and (ltp is not None and ltp >= Sell_FinalSL):
                print("Stop loss hit first time of " + self.symbol + ' at ' + str(ltp))
                fyerUtils.exit_position(ExitId)
                if Order2_Execution_Flag == 'True':
                    FinNifty_Sell_PE_Option.place_order_2(self)
                else:
                    print('-------------------------------------------------------------------------------')
                    print("Order 2 not executed due to Order2_Execution_Flag=False")
                    return
                intrade = 0
                Sell_FinalSL1 = 800
                while intrade == 0:
                    print('current time--', time.strftime('%H:%M:%S'))
                    symbol4 = {"symbols": self.symbol}
                    ltp = dataconfig.get_LTP(symbol4)
                    config1 = json.load(open(Constant.FINNIFTY_SELL_PE_OPTION))
                    entry_price = config1['limitPrice2']
                    stop_loss_2_percent = config1['stop_loss_2_percent']
                    current_price = ltp
                    sell_trailing_stop_loss_price1 = fyerUtils.Sell_trailing_stop_loss(current_price, int(entry_price),
                                                                                       int(stop_loss_2_percent))
                    time.sleep(2)
                    ExitId = {"id": "" + (self.symbol + '-' + self.productType) + ''}
                    if time.strftime('%H:%M') == Constant.TRADE_SQUARE_OFF:
                        fyerUtils.exit_position(ExitId)
                        print('Trade is Squared OFF')
                        return
                    print('-----------------------Machine2--SELLING CE mode with Order 2---------------------------')
                    print('Stop_loss2', Sell_FinalSL1)
                    Target2 = int(config1['limitPrice2']) - int(config1['target2'])
                    print('Target2', Target2)
                    if sell_trailing_stop_loss_price1 < Sell_FinalSL1:
                        Sell_FinalSL1 = sell_trailing_stop_loss_price1
                    if ltp is not None and ltp >= Sell_FinalSL1:
                        print('exit data', ExitId)
                        fyerUtils.exit_position(ExitId)
                        print("Stop loss hit second time of " + self.symbol + ' at ' + str(ltp))
                        return
                    elif ltp is not None and ltp <= Target2:
                        fyerUtils.exit_position(ExitId)
                        print("Profit booked in second go for " + self.symbol + ' at ' + str(ltp))
                        return
            elif (side == -1) and (ltp is not None and ltp <= Target1):
                print('ltp price in profit booking', ltp)
                fyerUtils.exit_position(ExitId)
                print("Profit booked in first go for " + self.symbol + ' at ' + str(ltp))
                return
            else:
                time.sleep(1)

    def get_LTP(self, symbol):
        try:
            fyerUtils = Fyers_Utilty()
            fyers = fyersModel.FyersModel(client_id=fyerUtils.client_id, token=fyerUtils.access_token, log_path="")
            ltp = fyers.quotes(symbol)['d'][0]['v']['lp']
            print('ltp of ', self.symbol, ' is ', ltp)
            return ltp
        except:
            print(traceback.print_stack())

    def place_order_2(self):
        side = -1
        classname = dataconfig.__class__.__name__
        fyerUtils = Fyers_Utilty()
        symbol = {"symbols": self.symbol}
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
            fyers = fyersModel.FyersModel(client_id=fyerUtils.client_id, token=fyerUtils.access_token, log_path="")
            while True:
                self.symbol = fyerUtils.get_CE_FNO_Data(classname)
                print('self.symbol22222-------', self.symbol)
                filterStock = self.symbol

                symbol2 = {"symbols": filterStock}
                filterStockPrice = dataconfig.get_LTP(symbol2)
                print(filterStock, dataconfig.get_LTP(symbol2))
                print('\033[94m-------------------------place_order 2---------------------------')

                print('current time--', time.strftime('%H:%M:%S'))

                if Constant.PAPER_TRADE == 'YES':
                    print('You are trading with PaperWork')
                else:
                    response = fyers.place_order(data2)
                    print('Order Placed  in place_order 2 with LTP ', filterStockPrice, response)
                self.config['symbol'] = self.symbol
                self.limitPrice2 = filterStockPrice
                self.limitPrice2 = filterStockPrice
                self.config['limitPrice2'] = self.limitPrice2
                with open(Constant.FINNIFTY_SELL_PE_OPTION, 'w') as f:
                    f.write(json.dumps(self.config))
                    f.close()
                print('Order Placed  in place_order 2 with LTP ', filterStockPrice, ' for -', self.symbol)
                return self.limitPrice2

        except:
            print(traceback.print_exc())


if __name__ == '__main__':
    dataconfig = FinNifty_Sell_PE_Option()

    dataconfig.place_order_1()
