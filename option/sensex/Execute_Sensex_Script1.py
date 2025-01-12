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
            if time.strftime('%H:%M') < Constant.TRADE_SQUARE_OFF:
                Execute_Sensex_Script.executeScript_sensex_ce_pe_script(self)
            else :
                return


if __name__ == '__main__':
    script = Execute_Sensex_Script()
    script.executeScript_sensex_ce_pe_script()
    # script.executeScript_sensex_ce_pe()
