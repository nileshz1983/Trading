import base64
import json, traceback
import os.path
import time
from fyers_apiv3 import fyersModel
from utils import Constant
from utils.Fyers_Utilty import Fyers_Utilty
import sys
import logging
from datetime import date, datetime

current_datetime = datetime.now()
formatted_time = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

LOG_FOLDER = "logs"
LOG_FILE = "Sensex_Sell_PE_Option.log"
os.makedirs(LOG_FOLDER, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_FOLDER, LOG_FILE),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

config = {'target1': '', 'quantity1': '', 'limitPrice1': '',
          'target2': '', 'quantity2': '', 'limitPrice2': '', 'symbol': '',
          'Order2_Execution_Flag': ''
          }


class Sensex_Sell_PE_Option:
    executionFlag = False

    @classmethod
    def set_flag(self, value: bool):
        self.executionFlag = value  # Update the flag value

    @classmethod
    def get_flag(self) -> bool:
        # print('self.executionFlag  inside get_flag', self.executionFlag)
        return self.executionFlag  # Return the current flag value

    def __init__(self) -> None:
        global config
        fyerUtils = Fyers_Utilty()

        try:
            if not os.path.join(os.getcwd().join(Constant.SENSEX_SELL_PE_OPTION.strip())):
                self.create_config_file()
                print("file not exists", os.getcwd())
            else:
                pass
                # print("file  exist", os.getcwd())
        except:
            print(traceback.print_exc())
        config = json.load(open(Constant.SENSEX_SELL_PE_OPTION))
        # print("\033[93mSell_config--", config)
        self.target1 = config['target1']
        self.target2 = config['target2']
        self.symbol = config['symbol']
        self.quantity1 = config['quantity1']
        self.quantity2 = config['quantity2']
        self.limitPrice1 = config['limitPrice1']
        self.limitPrice2 = config['limitPrice2']
        self.Order2_Execution_Flag = config['Order2_Execution_Flag']
        self.config = config
        self.model = None
        if self.target1 == '' or self.target2 == '' or self.quantity1 == '' or self.quantity2 == '':
            print(self.target1, 'elf.target2-', self.target2,
                  'self.quantity1-', self.quantity1, 'self.quantity2', self.quantity2)
            print('please enter all the details in the SENSEX_SELL_PE_OPTION.json file')
            exit()

    def create_config_file(self):
        file = json.dumps(config, indent=10)
        with open("../../config/SENSEX_SELL_PE_OPTION.json", "w") as f:
            f.write(file)
            f.close()

    def place_order_1(self):
        global counter, Sell_FinalSL, Buy_FinalSL, symbol2
        fyerUtils = Fyers_Utilty()
        classname = dataconfig.__class__.__name__
        fyers = fyersModel.FyersModel(client_id=fyerUtils.client_id, token=fyerUtils.access_token, log_path="")

        side = -1
        intrade = 1
        productType = Constant.PRODUCT_TYPE
        self.symbol = fyerUtils.get_PE_FNO_Data(classname)
        filterStock = self.symbol
        symbol2 = {"symbols": filterStock}
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
            "offlineOrder": False,
            "orderTag": "tag1"
        }
        try:
            while True:

                self.config['symbol'] = self.symbol
                self.limitPrice1 = filterStockPrice
                print('filterStockPrice---', filterStockPrice)
                self.config['limitPrice1'] = self.limitPrice1
                with open(Constant.SENSEX_SELL_PE_OPTION, 'w') as f:
                    f.write(json.dumps(self.config))
                    f.close()
                config4 = json.load(open(Constant.SENSEX_SELL_PE_OPTION))
                print('\033[92m-------------------------place_order 1---------------------------')
                logging.info("-----------------------------Trading Time--" + formatted_time + '------------------')
                # print('current time--', time.strftime(" %H:%M:%S"))
                logging.info('Order Placed  in place_order 1  %s %s', self.symbol, filterStockPrice)

                if Constant.PAPER_TRADE == 'YES':
                    print('You are trading with PaperWork')
                    logging.info("You are trading with PaperWork.")
                else:
                    response = fyers.place_order(data1)
                    print('Order Placed  in place_order 1 with LTP ', filterStockPrice, response)
                    logging.info('Order Placed  in place_order 1 with LTP  %s %s', filterStockPrice, response)

                # print('Order Placed  in place_order 1 with LTP ', ltp)
                break
        except:
            print(traceback.print_exc())
        Sell_FinalSL = 2000.0
        fyerUtils = Fyers_Utilty()
        while intrade == 1:
            # print('current time--', time.strftime('%H:%M:%S'))

            ltp = dataconfig.get_LTP(symbol2)
            # ltp = None
            time.sleep(Constant.WAITING_TIME)
            config1 = json.load(open(Constant.SENSEX_SELL_PE_OPTION))
            entry_price = config1['limitPrice1']
            Order2_Execution_Flag = config1['Order2_Execution_Flag']
            # print('Order2_Execution_Flag -- ', Order2_Execution_Flag)
            stop_loss_1_percent = config1['stop_loss_1_percent']
            current_price = ltp
            sell_trailing_stop_loss_price = fyerUtils.Sell_trailing_stop_loss_PE(current_price, int(entry_price),
                                                                              int(stop_loss_1_percent))
            ExitId = {"id": "" + (self.symbol + '-' + productType) + ''}
            if time.strftime('%H:%M') == Constant.TRADE_SQUARE_OFF:
                fyerUtils.exit_position(ExitId)
                print('Trade is Squared OFF')
                logging.info("Trade is Squared OFF at - %s", ltp)
                return
            # print('\033[93m---------------------Sensex_Sell_PE_Option---------------------------')
            # print('current time in Sensex_Sell_PE_Option --', time.strftime('%H:%M:%S'))
            print('Stop_loss in Sensex_Sell_PE_Option -- ', Sell_FinalSL)
            Target1 = int(config1['limitPrice1']) - int(config1['target1'])
            if Target1 < 0:
                Target1 = 0
                print('Target in Sensex_Sell_PE_Option --', Target1)
            else:
                print('Target in Sensex_Sell_PE_Option --', Target1)
            # time.sleep(1)
            # ltp = 368
            if sell_trailing_stop_loss_price < Sell_FinalSL:
                Sell_FinalSL = sell_trailing_stop_loss_price
            if (side == -1) and (ltp is not None and ltp >= Sell_FinalSL):
                self.config['symbol'] = None
                self.config['limitPrice1'] = 0
                with open(Constant.SENSEX_SELL_PE_OPTION, 'w') as f:
                    f.write(json.dumps(self.config))
                    f.close()
                print("Stop loss hit first time of " + self.symbol + ' at ' + str(ltp))
                logging.info("Stop loss hit first time of " + self.symbol + ' at ' + str(ltp))
                executionFlag = True
                if executionFlag:
                    Sensex_Sell_PE_Option.set_flag(True)
                    Sensex_Sell_PE_Option.get_flag()
                    # print('Sensex_Sell_PE_Option.get_flag()----', Sensex_Sell_PE_Option.get_flag())
                    fyerUtils.exit_position(ExitId)
                if Order2_Execution_Flag == 'True':
                    Sensex_Sell_PE_Option.place_order_2(self)
                else:
                    print('-------------------------------------------------------------------------------')
                    print("Order 2 not executed due to Order2_Execution_Flag=False")
                    return
                intrade = 0
                Sell_FinalSL1 = 800
                while intrade == 0:
                    # print('current time--', time.strftime('%H:%M:%S'))
                    symbol4 = {"symbols": self.symbol}
                    ltp = dataconfig.get_LTP(symbol4)
                    config1 = json.load(open(Constant.SENSEX_SELL_PE_OPTION))
                    entry_price = config1['limitPrice2']
                    stop_loss_2_percent = config1['stop_loss_2_percent']
                    current_price = ltp
                    sell_trailing_stop_loss_price1 = fyerUtils.Sell_trailing_stop_loss(current_price, int(entry_price),
                                                                                       int(stop_loss_2_percent))
                    time.sleep(2)
                    ExitId = {"id": "" + (self.symbol + '-' + productType) + ''}
                    if time.strftime('%H:%M') == Constant.TRADE_SQUARE_OFF:
                        fyerUtils.exit_position(ExitId)
                        print('Trade is Squared OFF')
                        logging.info("Trade is Squared OFF at - %s ", ltp)
                        return
                    print('-----------------------Machine2--SELLING PE mode with Order 2---------------------------')
                    print('Stop_loss2', Sell_FinalSL1)
                    Target2 = int(config1['limitPrice2']) - int(config1['target2'])
                    if sell_trailing_stop_loss_price1 < Sell_FinalSL1:
                        Sell_FinalSL1 = sell_trailing_stop_loss_price1
                    if ltp is not None and ltp >= Sell_FinalSL1:
                        print('exit data', ExitId)
                        self.config['symbol'] = None
                        self.config['limitPrice2'] = 0
                        with open(Constant.SENSEX_SELL_PE_OPTION, 'w') as f:
                            f.write(json.dumps(self.config))
                            f.close()
                        fyerUtils.exit_position(ExitId)
                        print("Stop loss hit second time of " + self.symbol + ' at ' + str(ltp))
                        logging.info("Stop loss hit second time of " + self.symbol + ' at ' + str(ltp))
                        return
                    elif ltp is not None and ltp <= Target2:
                        self.config['symbol'] = None
                        self.config['limitPrice2'] = 0
                        with open(Constant.SENSEX_SELL_PE_OPTION, 'w') as f:
                            f.write(json.dumps(self.config))
                            f.close()
                            executionFlag = True
                            if executionFlag:
                                Sensex_Sell_PE_Option.set_flag(True)
                                Sensex_Sell_PE_Option.get_flag()
                                # print('Sensex_Sell_PE_Option.get_flag()----', Sensex_Sell_PE_Option.get_flag())
                        fyerUtils.exit_position(ExitId)
                        print("Profit booked in second go for " + self.symbol + ' at ' + str(ltp))
                        logging.info("Profit booked in second go for " + self.symbol + ' at ' + str(ltp))
                        return
            elif (side == -1) and (ltp is not None and ltp <= Target1):
                print('ltp price in profit booking', ltp)
                self.config['symbol'] = None
                self.config['limitPrice1'] = 0
                with open(Constant.SENSEX_SELL_PE_OPTION, 'w') as f:
                    f.write(json.dumps(self.config))
                    f.close()
                fyerUtils.exit_position(ExitId)
                print("Profit booked in first go for " + self.symbol + ' at ' + str(ltp))
                logging.info("Profit booked in first go for " + self.symbol + ' at ' + str(ltp))
                return
            else:
                time.sleep(1)

    def get_LTP(self, symbol):
        try:
            fyerUtils = Fyers_Utilty()
            fyers = fyersModel.FyersModel(client_id=fyerUtils.client_id, token=fyerUtils.access_token, log_path="")
            ltp = fyers.quotes(symbol)['d'][0]['v']['lp']
            print('\033[93m---------------------Sensex_Sell_PE_Option---------------------------')
            print('current time in Sensex_Sell_PE_Option --', time.strftime('%H:%M:%S'))
            print('ltp of ', self.symbol, ' is ', ltp)
            return ltp
        except:
            print(traceback.print_stack())

    def place_order_2(self):
        print('\033[94m-------------------------place_order 2---------------------------')

        # print('current time--', time.strftime('%H:%M:%S'))
        side = -1
        classname = dataconfig.__class__.__name__
        fyerUtils = Fyers_Utilty()
        self.symbol = fyerUtils.get_CE_FNO_Data(classname)
        filterStock = self.symbol
        symbol2 = {"symbols": filterStock}
        filterStockPrice = dataconfig.get_LTP(symbol2)
        data2 = {
            "symbol": self.symbol,
            "qty": self.quantity2,
            "type": 1,
            "side": side,
            "productType": Constant.PRODUCT_TYPE,
            "limitPrice": filterStockPrice,
            "stopPrice": 0,
            "validity": "DAY",
            "disclosedQty": 0,
            "offlineOrder": False,
            "orderTag": "tag1"
        }

        try:
            fyers = fyersModel.FyersModel(client_id=fyerUtils.client_id, token=fyerUtils.access_token, log_path="")
            while True:

                if Constant.PAPER_TRADE == 'YES':
                    print('You are trading with PaperWork')
                    logging.info("You are trading with PaperWork.")
                else:
                    response = fyers.place_order(data2)
                    print('Order Placed  in place_order 2 with LTP ', filterStockPrice, response)
                    logging.info('Order Placed  in place_order 2 with LTP  %s %s', filterStockPrice, response)
                self.config['symbol'] = self.symbol
                self.limitPrice2 = filterStockPrice
                self.limitPrice2 = filterStockPrice
                self.config['limitPrice2'] = self.limitPrice2
                with open(Constant.SENSEX_SELL_PE_OPTION, 'w') as f:
                    f.write(json.dumps(self.config))
                    f.close()
                print('Order Placed  in place_order 2 with LTP ', filterStockPrice, ' for -', self.symbol)
                logging.info('Order Placed  in place_order 2 with LTP %s %s', filterStockPrice, self.symbol)
                return self.limitPrice2

        except:
            print(traceback.print_exc())


if __name__ == '__main__':
    dataconfig = Sensex_Sell_PE_Option()

    dataconfig.place_order_1()
