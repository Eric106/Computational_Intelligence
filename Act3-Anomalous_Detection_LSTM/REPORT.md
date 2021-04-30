# ACT 3 - Anomalous Detection LSTM

    Eric Gómez - A01378838
    Felipe Osornio - A01377154  
    Rafael Moreno - A01378916  
    Uriel Pineda - A01379633
    Hector Hernandez - A01374009

---
## Introduction
- que es LSTM mas
- breve ARIMA

KEY WORDS:
epoch = one epoch pass through the neural network all the training dataset divided in batchs
batch_size = how many item/values inside the batch

---
## Methodology


- how CPU & exec_time
```python
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
```
- modularize ARIMA and LSTM to call it easy
```python
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
    print('All dataset st_deviation: ', round(stdev(df[column].tolist()),4))
    print('Predicted dataset st_deviation: ',round(stdev(prediction),4))


def run_lstm(file:str, column:str):
    global IS_Process_end
    IS_Process_end = False
    df = csv_to_df(file)
    LSTM_config = {
        'test_size': 0.2,
        'is_normalized': True,
        'epochs': 40,
        'batch_size': 80,
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
    print('All dataset st_deviation: ', round(stdev(df[column].tolist()),4))
    print('Predicted dataset st_deviation: ',round(stdev(prediction),4))
```
- how to decide the ARIMA (graficas) and LSTM run allot to set config (refrence to FINDS) values & normalize(paper que mando) data


---
## Finds

```python
CPU utilization:  21.72 %
All dataset average:  0.081
Predicted dataset average:  0.104
All dataset st_deviation:  0.0402
Predicted dataset st_deviation:  0.0308
ARIMA TIME:  87.1 s
```
```python
CPU utilization:  60.42 %
All dataset average:  0.081
Predicted dataset average:  0.9853
All dataset st_deviation:  0.0402
Predicted dataset st_deviation:  1.4887
LSTM TIME: 60.54 s
```
- LSTM epoch*2 >= batch_size >= epoch 
- comparaciones outputs
    <> +batch_size mayor ruido y menor tiempo de procesamiento por cada item/value
    <> -batch_size menor ruido pero mayor tiempo de procesamiento por cada item/value
    <> LSTM +cpu -exec_time
    <> ARIMA -cpu +exec_time
    <> fig1.LSTM +epoch -(minimum loss error function) --> +epochs mayor precision
    <> fi2.LSTM +good prediction
    <> ARIMA(classical inference PML) la prediccion tiene unos datos menos dispersos (std_dev) y el promedio de valore es mas parecida al dataset original
    <> LSTM la prediccion arroja datos mas dispersos y en promedio tiene valores mas altos que el dataset original.
 
---
## Conclusion
- ARIMA tiende a generar valores estimados menos dispersos y un poco mas acercados al data set original, debido a que es un metodo de inferencia clasica.
- LSTM jala pero entre mas epochs le pongas mayor sera la presicion
- para un analisis inicial de anomalias es una buena herramienta ya que puedes darte una buen idea con pocas "epochs"
- y lo unico negativo seria que el LSTM consume mas 'cpu' que ARIMA

