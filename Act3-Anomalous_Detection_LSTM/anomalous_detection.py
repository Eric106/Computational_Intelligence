from time import time
from pandas import read_csv
from termcolor import  colored
from modules import run_arima as ARIMA
from modules import run_lstm as LSTM

ARIMA_config = {
    'test_size':0.2,
    'AR':1,
    'MA':30,
    'target_method':'PML',
    'h':100,
    'pv':40
}

LSTM_config = {
    'test_size':0.2,
    'is_normalized':True,
    'epochs':3,
    'batch_size':50,
    'validation_split':0.05,
    'loss':'mean_squared_error',
    'optimizer':'rmsprop',
    'metrics':['mean_squared_error', 'mean_absolute_error', 'mean_absolute_percentage_error']
}

def exec_time(func, args:list) -> tuple:
    '''
    Function that measures execution time of a given function
    '''
    error = None
    intiTime = time()
    try:
        func(*args)
    except Exception as e:
        error = e
    elapsedTime = round(time()-intiTime, 2)
    if elapsedTime >= 60:
        elapsedTime = str(elapsedTime/60) + 'm'
    else:
        elapsedTime = str(elapsedTime)+'s'
    return elapsedTime, error


def csv_to_df(csv_file:str):
    '''returns numpy array of values from a dataFrame)'''
    print('Loading data... ')
    df = read_csv(csv_file, parse_dates=[0], infer_datetime_format=True)
    return df


def run_arima(file:str, column:str):
    df = csv_to_df(file)
    ARIMA.run(df, column, ARIMA_config)


def run_lstm(file:str, column:str):
    df = csv_to_df(file)
    LSTM.run(df,column,LSTM_config)

def main():
    paths = {
        'vibration':['Averaged_BearingTest_Dataset.csv','Bearing1']
    }
    div = colored('\n===========================================','magenta')
    for solution in ['ARIMA','LSTM'][:1]:
        print(colored(solution,'magenta'),div)
        error = None
        if solution == 'ARIMA':
            elapsedTime, error = exec_time(run_arima, args=paths['vibration'])
        elif solution == 'LSTM':
            elapsedTime, error = exec_time(run_lstm, args=paths['vibration'])
        if error != None:
            print("ERROR: ",error)
        print("\n"+solution+" TIME --->", elapsedTime)


main()