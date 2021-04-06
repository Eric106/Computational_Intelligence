from time import time
import pyflux as pf
import matplotlib.pyplot as plt
from . import arima_utils as au
from pandas import DataFrame
from termcolor import  colored

div1 = colored('\n********************************************************************','green')
div2 = colored('\n===========================================','magenta')

#read data and split and test and training set
def set_up(df:DataFrame, ar:int, ma:int ,target_col:str):
    global DF, AR, MA, TAR_COL
    DF, AR, MA, TAR_COL = df, ar, ma, target_col


def get_pacf_acf(data: DataFrame, target_col: str):
    print(div1,colored('\n ADF Test Statistic','green'))
    au.adfuller_test(data[target_col])

    print(div1,colored('\n Plot Original Series','green'))
    au.plot_series(data[target_col],'Original Series')

    print(div1,colored('\n Plot Partial Autocorrelation','green'))
    au.plot_pacf(data[target_col])

    print(div1,colored('\n Plot Autocorrelation','green'))
    au.plot_acf(data[target_col])
    

def try_models(inference: str, h: int, pv: int):
    # https://pyflux.readthedocs.io/en/latest/classical.html
    # https://pyflux.readthedocs.io/en/latest/bayes.html
    inf_types = {
        "classical":['MLE','PML'],
        "bayesian":['Laplace','M-H']
        # "bayesian":['Laplace','BBVI']
    }
    dict_times = {'model_type':[],'time':[], 'forecast_mean_'+TAR_COL:[]}
    for i_method in inf_types[inference]:
        print(div2,colored('\n '+inference+': '+i_method,'magenta'))
        intiTime = time()
        mean = try_model(i_method, h, pv)
        elapsedTime = round(time()-intiTime, 2)
        elapsedTime = round(elapsedTime/60,4)
        print("\nTiempo del proceso --->", elapsedTime)
        dict_times['model_type'].append(inference+': '+i_method)
        dict_times['time'].append(elapsedTime)
        dict_times['forecast_mean_'+TAR_COL].append(mean)
    return DataFrame(dict_times)


def try_model(target_method: str, h: int, pv: int):
    arima_model = pf.ARIMA(data=DF, ar=AR, ma=MA, integ=0, target=TAR_COL)
    x = arima_model.fit(method=target_method)
    print(x.summary())
    '''
    Use the data that you have and see that predictions fit with the values that you have in the dataset.
    h = How many steps to forecast ahead
    past_values: How many past datapoints to plot
    '''
    arima_model.plot_fit()

    # arima_model.plot_predict_is(h=h, past_values=pv)

    arima_model.plot_predict(h=h, past_values=pv)

    fcast = arima_model.predict(h=h)
    print(fcast)
    del arima_model, x
    return fcast[TAR_COL].mean()

