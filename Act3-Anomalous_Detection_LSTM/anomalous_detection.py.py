from time import time
from pandas import read_csv
from modules import run_arima




def main():
    paths = {
        "vibration":"Averaged_BearingTest_Dataset.csv"
    }

    intiTime = time()

    

    elapsedTime = round(time()-intiTime, 2)
    elapsedTime = str(elapsedTime/60) + \
        "m" if elapsedTime >= 60 else str(elapsedTime)+"s"
    print("\nGENERAL TIME --->", elapsedTime)


main()