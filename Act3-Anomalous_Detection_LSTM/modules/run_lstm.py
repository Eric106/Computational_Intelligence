from time import time
from . import lstm_utils as lu # pylint: disable=relative-beyond-top-level
from pandas import DataFrame

def get_test_idx(len_values:int, slice_size: float):
    idx_cut = int((len_values)*(1-slice_size))
    return 0, idx_cut-1, idx_cut, len_values-1


def run(df:DataFrame, target_value:str, dict_config:dict):
    '''Runs the ANN with the selected config and data '''
    data = df[target_value].values
    test_size = dict_config['test_size']
    is_normalized = dict_config['is_normalized']
    epochs = dict_config['epochs']
    batch_size = dict_config['batch_size']
    validation_split = dict_config['validation_split']
    loss = dict_config['loss']
    optimizer = dict_config['optimizer']
    metrics = dict_config['metrics']

    train_start, train_end, test_start, test_end = get_test_idx(len(data), test_size)
    sequence_length= 100
    global_start_time = time()

    print('Prepare data... ')
    # train on first 700 samples and test on next 300 samples (test set has anomaly)
    X_train, y_train, X_test, y_test = lu.prepare_data(
        data, train_start, train_end, test_start, test_end, sequence_length, is_normalized)

    print('Genetate Model... ')
    model = lu.generate_model(sequence_length, loss, optimizer, metrics)

    print('Training data... ')
    history = lu.fit(model, X_train, y_train, batch_size,
                     epochs, validation_split, global_start_time)

    print('Plot Fit results... ')
    lu.plot_training_results(history)

    print("Predicting...")
    predicted = lu.predict(model, X_test)

    print('Plot Predict results... ')
    lu.plot_model_result(global_start_time, y_test, predicted)

    return predicted


# target_value ='cpu'
# data_path='resources/cpu-full-b-1-1.csv'
# is_normalized=True
# epochs = 3
# batch_size = 50
# validation_split=0.05
# loss='mean_squared_error'
# optimizer='rmsprop'
# metrics=['mean_squared_error', 'mean_absolute_error', 'mean_absolute_percentage_error']

# predicted = run(data_path,is_normalized, target_value,epochs, batch_size,validation_split, loss, optimizer, metrics)
