import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

from keras.models import Sequential
from keras.layers.recurrent import LSTM
from keras.layers.core import Dense, Activation, Dropout


def load_data(csv_file,target_value):
    print('Loading data... ')
    data_b = pd.read_csv(csv_file,
                         parse_dates=[0], infer_datetime_format=True)
    data = data_b[target_value].values
    return data

def normalize(result):
    result_mean = result.mean()
    result_std = result.std()
    result -= result_mean
    result /= result_std
    return result, result_mean

def prepare_data(data, train_start, train_end, test_start, test_end,sequence_length, is_normalized):
    print("Length of Data", len(data))

    # training data
    print("Creating training data...")
    temp = []
    for index in range(train_start, train_end - sequence_length):
        temp.append(data[index: index + sequence_length])
    temp = np.array(temp)
    if is_normalized == True:
        temp, temp_mean = normalize(temp)
    print("Training data shape  : ", temp.shape)

    train = temp[train_start:train_end, :]
    np.random.shuffle(train)
    X_train = train[:, :-1]
    y_train = train[:, -1]

    # test data
    print("Creating test data...")

    temp = []
    for index in range(test_start, test_end - sequence_length):
        temp.append(data[index: index + sequence_length])
    temp = np.array(temp)
    if is_normalized==True:
        temp, temp_mean = normalize(temp)

    print("Test data shape  : {}".format(temp.shape))

    X_test = temp[:, :-1]
    y_test = temp[:, -1]

    print("Shape X_train", np.shape(X_train))
    print("Shape X_test", np.shape(X_test))

    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

    print("Shape X_train", np.shape(X_train))
    print("Shape X_test", np.shape(X_test))

    return X_train, y_train, X_test, y_test

def generate_model(sequence_length, loss, optimizer, metrics):
    model = Sequential()

    # First LSTM layer defining the input sequence length
    model.add(LSTM(input_shape=(sequence_length - 1, 1),
                   units=32,
                   return_sequences=True))
    model.add(Dropout(0.2))

    # Second LSTM layer with 128 units
    model.add(LSTM(units=128,
                   return_sequences=True))
    model.add(Dropout(0.2))

    # Third LSTM layer with 100 units
    model.add(LSTM(units=100,
                   return_sequences=False))
    model.add(Dropout(0.2))

    # Densely-connected output layer with the linear activation function
    model.add(Dense(units=1))
    model.add(Activation('linear'))

    model.compile(loss=loss, optimizer=optimizer, metrics=metrics)

    return model

def fit(model,X_train, y_train, batch_size, epochs, validation_split,global_start_time):
    print("Training...")
    history = model.fit(
        X_train, y_train,verbose=1,
        batch_size=batch_size, epochs=epochs, validation_split=validation_split)
    print('Training duration:{}'.format(time.time() - global_start_time))
    return history


def predict(model, set_values_toPredict):
    predicted = model.predict(set_values_toPredict)

    print("Reshaping predicted")
    predicted = np.reshape(predicted, (predicted.size,))
    return predicted


def plot_training_results (history):
    # plot the training losses
    fig, ax = plt.subplots(figsize=(14, 6), dpi=80)
    ax.plot(history.history['loss'], 'b', label='Train', linewidth=2)
    ax.plot(history.history['val_loss'], 'r', label='Validation', linewidth=2)
    ax.set_title('Model loss', fontsize=16)
    ax.set_ylabel('Loss (mae)')
    ax.set_xlabel('Epoch')
    ax.legend(loc='upper right')
    plt.savefig('figures/cpu.plot.training.result.png')

def plot_model_result(global_start_time, y_test, predicted):
    try:
        plt.figure(figsize=(20, 8))
        plt.plot(y_test[:len(y_test)], 'b', label='Observed')
        plt.plot(predicted[:len(y_test)], 'g', label='Predicted')
        plt.plot(((y_test - predicted) ** 2), 'r', label='Root-mean-square deviation')
        plt.legend()
        plt.savefig('figures/cpu.plot.model.result.png')
    except Exception as e:
        print("plotting exception")
        print(str(e))
    print('Training duration:{}'.format(time.time() - global_start_time))



def run(data_path,is_normalized,target_value, epochs, batch_size,validation_split, loss, optimizer, metrics):
    sequence_length= 100
    global_start_time = time.time()

    print('Loading data... ')
    data = load_data(data_path,target_value)

    print('Prepare data... ')
    # train on first 700 samples and test on next 300 samples (test set has anomaly)
    X_train, y_train, X_test, y_test = prepare_data(data, 0, 600, 400, 660,sequence_length,is_normalized)

    print('Genetate Model... ')
    model = generate_model(sequence_length,loss, optimizer, metrics)

    print('Training data... ')
    history = fit(model, X_train, y_train,batch_size, epochs, validation_split,global_start_time)

    print('Plot Fit results... ')
    plot_training_results(history)

    print("Predicting...")
    predicted = predict(model,X_test)

    print('Plot Predict results... ')
    plot_model_result(global_start_time, y_test, predicted)

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
