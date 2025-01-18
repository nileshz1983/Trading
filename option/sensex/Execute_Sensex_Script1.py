import threading
from concurrent.futures import ThreadPoolExecutor
import time
import subprocess
from pathlib import Path
from option.sensex.Sensex_Sell_CE_Option import Sensex_Sell_CE_Option
from option.sensex.Sensex_Sell_PE_Option import Sensex_Sell_PE_Option
from utils import Constant
from utils.Fyers_Utilty import Fyers_Utilty


class Execute_Sensex_Script:
    def __init__(self) -> None:
        a = Sensex_Sell_CE_Option()
        b = Sensex_Sell_PE_Option()

    def executeScript_sensex_ce_pe_script(self):
        script_path = ("C:\\Users\ADMIN\Documents\ALGO_TRADE_FYERS_API\Python_Trade5_12Dec\option\sensex"
                       "\Sensex_Sell_CE_Option.py")
        script_path1 = ("C:\\Users\ADMIN\Documents\ALGO_TRADE_FYERS_API\Python_Trade5_12Dec\option\sensex"
                        "\Sensex_Sell_PE_Option.py")

        # Run both scripts in parallel
        process_one = subprocess.Popen(["py", script_path])
        time.sleep(2)
        process_two = subprocess.Popen(["py", script_path1])

        # Wait for both processes to complete
        process_one.wait()
        process_two.wait()

        print("Both scripts have finished execution.")
        Sell_CE_Option = Sensex_Sell_CE_Option()
        Sell_PE_Option = Sensex_Sell_PE_Option()

        # print('Sensex_Sell_CE_Option().executionFlag', Sell_CE_Option.get_flag())
        # print('Sensex_Sell_PE_Option().executionFlag', Sell_PE_Option.get_flag())
        if (Sell_CE_Option.get_flag() == False) & (Sell_PE_Option.get_flag() == False):
            # if TRADE_SQUARE_OFF is greater tha 3.25 then script will execute only once
            if time.strftime('%H:%M') < Constant.TRADE_SQUARE_OFF:
                Execute_Sensex_Script.executeScript_sensex_ce_pe_script(self)
            else:
                print('Trade tomorrow as trading time is over at', Constant.TRADE_SQUARE_OFF)
                return


if __name__ == '__main__':

    Trade = True
    while Trade:
        print('Current Time -----', time.strftime('%H:%M'))
        time.sleep(5)
        if time.strftime('%H:%M') >= Constant.TRADE_EXECUTION_TIME:
            script = Execute_Sensex_Script()
            script.executeScript_sensex_ce_pe_script()
            Trade = False
