
import pyflux as pf
import matplotlib.pyplot as plt
from . import arima_utils as au
from pandas import DataFrame

#read data and split and test and training set
def get_pacf_acf(data: DataFrame, target_col: str):
    au.adfuller_test(data[target_col])

    au.plot_series(data[target_col],'Original Series')

    au.plot_pacf(data[target_col])

    au.plot_acf(data[target_col])

def get_arima(data: DataFrame, target_col: str, p: int, q: int):
    # Define the model
    model = pf.ARIMA(data=data,
                    ar=p, ma=q, integ=0, target=target_col)
    return model

def try_models(arima_model):              
    x = arima_model.fit("PML")

    #https://pyflux.readthedocs.io/en/latest/bayes.html
    print(x.summary())

    print(x.scores)


    model.plot_fit()
    plt.show()

    '''
    Use the data that you have and see that predictions fit with the values that you have in the dataset.
    h = How many steps to forecast ahead
    past_values: How many past datapoints to plot
    '''
    model.plot_predict_is(h=30)
    plt.show()

    model.plot_predict_is(h=100, past_values=40)
    plt.show()

    #How many steps to forecast ahead
    model.plot_predict(h=200, past_values=40)
    plt.show()

    #How many steps to forecast ahead
    fcast = model.predict(h=200)
    print(fcast)



