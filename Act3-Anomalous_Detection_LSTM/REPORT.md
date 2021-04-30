# ACT 3 - Anomalous Detection LSTM

    Eric Gómez - A01378838
    Felipe Osornio - A01377154  
    Rafael Moreno - A01378916  
    Uriel Pineda - A01379633
    Hector Hernandez - A01374009

---
## Introduction
- que es LSTM
- breve ARIMA

KEY WORDS:
epoch = one epoch pass through the neural network al the training dataset divided in batchs
batch_size = how many item/values inside the batch

---
## Methodology

- how CPU & exec_time
- how to decide the ARIMA (graficas) and LSTM run allot to set config (refrence to FINDS) values & normalize(paper que mando) data
- 



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

