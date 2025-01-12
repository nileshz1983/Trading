import base64
import hmac
import traceback

from fyers_api import fyersModel

from login.DataConfig_Validation import DataConfig_Validation


class PlacementOrder:
    def placeorderfyer(self):


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
            "limitPrice":0,
            "stopPrice":0,
            "validity": "DAY",
            "disclosedQty": 0,
            "offlineOrder": "False",
            "stopLoss": 0,
            "takeProfit": 0
        }
        try:
            return DataConfig_Validation.get_model().place_order(data1)
        except:
           traceback.print_stack()

        print('response', DataConfig_Validation.get_model(self).place_order(data1))


if __name__ == '__main__':
    order = PlacementOrder()
    #print('generate_token',order.generate_token())
    #print(order.get_profile())
    print('placeorderfyer',order.placeorderfyer())
