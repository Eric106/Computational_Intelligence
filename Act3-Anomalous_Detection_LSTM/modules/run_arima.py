import pyflux as pf
from . import arima_utils as au # pylint: disable=relative-beyond-top-level
from pandas import DataFrame
from termcolor import  colored

div1 = colored('\n********************************************************************','green')


def slice_dataFrame(df: DataFrame, slice_size: float):
    idx_cut = int((df.shape[0])*(1-slice_size))
    return df.iloc[:idx_cut], df.iloc[idx_cut:]


def get_pacf_acf(data: DataFrame, target_col: str):
    # print(div1,colored('\n ADF Test Statistic','green'))
    # au.adfuller_test(data[target_col])

    print(div1,colored('\n Plot Original Series','green'))
    au.plot_series(data[target_col],'Original Series')

    print(div1,colored('\n Plot Partial Autocorrelation','green'))
    au.plot_pacf(data[target_col])

    print(div1,colored('\n Plot Autocorrelation','green'))
    au.plot_acf(data[target_col])
    

def try_model(DF:DataFrame, TAR_COL:str, target_method:str, AR:int, MA:int, h:int, pv:int):
    arima_model = pf.ARIMA(data=DF, ar=AR, ma=MA, integ=0, target=TAR_COL)
    x = arima_model.fit(method=target_method)
    print(x.summary())
    '''
    Use the data that you have and see that predictions fit with the values that you have in the dataset.
    h = How many steps to forecast ahead
    past_values: How many past datapoints to plot
    '''
    # arima_model.plot_fit()

    # arima_model.plot_predict_is(h=h, past_values=pv)

    arima_model.plot_predict(h=h, past_values=pv)

    fcast = arima_model.predict(h=h)
    print(fcast)
    del arima_model, x
    return fcast[TAR_COL].tolist()


def run(df:DataFrame, target_col:str, dict_config:dict):
    test_size = dict_config['test_size']
    AR = dict_config['AR']
    MA = dict_config['MA']
    target_method = dict_config['target_method']
    h = dict_config['h']
    pv = dict_config['pv']
    train_df, test_df = slice_dataFrame(df, test_size)
    get_pacf_acf(train_df, target_col)
    prediction = try_model(test_df, target_col, target_method, AR, MA, h, pv)
    return prediction
