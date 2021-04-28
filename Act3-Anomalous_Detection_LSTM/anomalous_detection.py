from threading import Thread
from time import time, sleep
from statistics import mean, stdev
from psutil import cpu_percent
from pandas import read_csv, DataFrame
from termcolor import  colored
from modules import run_arima as ARIMA
from modules import run_lstm as LSTM


def exec_time(func, args:list) -> str:
    '''
    Function that measures execution time of a given function
    '''
    intiTime = time()
    try:
        func(*args)
    except Exception as e:
        print('ERROR: ',e)
    elapsedTime = round(time()-intiTime, 2)
    return str(elapsedTime)+'s'


def get_cpu_utilization() -> Thread:

    def cpu_util():
        cpu_data = []
        while(not IS_Process_end):
            sleep(1)
            cpu_data.append(cpu_percent())
        print('CPU utilization: ', round(mean(cpu_data),2),'%')

    return Thread(
        target=cpu_util
    )


def csv_to_df(csv_file:str) -> DataFrame:
    '''returns numpy array of values from a dataFrame)'''
    print('Loading data... ')
    df = read_csv(csv_file, parse_dates=[0], infer_datetime_format=True)
    return df


def run_arima(file:str, column:str):
    global IS_Process_end
    IS_Process_end = False
    df = csv_to_df(file)
    ARIMA_config = {
        'test_size': 0.2,
        'AR': 1,
        'MA': 50,
        'target_method': 'PML',
        'h': 100,
        'pv': 40
    }
    cpu_thread = get_cpu_utilization()
    cpu_thread.start()
    prediction = ARIMA.run(df, column, ARIMA_config)
    IS_Process_end = True
    cpu_thread.join()
    print('All dataset average: ', round(mean(df[column].tolist()),4))
    print('Predicted dataset average: ', round(mean(prediction),4))
    print('All dataset st_deviation: ',round(stdev(df[column].tolist()),4))
    print('Predicted dataset st_deviation: ',round(stdev(prediction),4))


def run_lstm(file:str, column:str):
    global IS_Process_end
    IS_Process_end = False
    df = csv_to_df(file)
    LSTM_config = {
        'test_size': 0.2,
        'is_normalized': True,
        'epochs': 10,
        'batch_size': 10,
        'validation_split': 0.05,
        'loss': 'mean_squared_error',
        'optimizer': 'rmsprop',
        'metrics': ['mean_absolute_percentage_error']
    }
    cpu_thread = get_cpu_utilization()
    cpu_thread.start()
    prediction = LSTM.run(df, column, LSTM_config)
    IS_Process_end = True
    cpu_thread.join()
    print('All dataset average: ', round(mean(df[column].tolist()),4))
    print('Predicted dataset average: ', round(mean(prediction),4))
    print('All dataset st_deviation: ',round(stdev(df[column].tolist()),4))
    print('Predicted dataset st_deviation: ',round(stdev(prediction),4))


def main():
    paths = {
        'vibration':['Averaged_BearingTest_Dataset.csv','Bearing1']
    }
    div = colored('\n===========================================','magenta')
    for solution in ['ARIMA','LSTM']:
        print(div,colored('\n'+solution,'magenta'),div)

        if solution == 'ARIMA':
            elapsedTime = exec_time(run_arima, args=paths['vibration'])
        elif solution == 'LSTM':
            elapsedTime = exec_time(run_lstm, args=paths['vibration'])

        print(solution,"TIME --->", elapsedTime)


main()
