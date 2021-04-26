# ACT 1 -  Anomalous Detection

## Considerations

After cloning this repo, dowload the file [http.log](https://experiencia21.tec.mx/courses/112876/files/44700556/download?download_frd=1) in the same folder of `anomalous_detection.py`.

## Execution

First make sure that the requirements are correctly installed. The dependencies can be installed via: 

`Anaconda`

```shell
~$ conda install -c defaults -c conda-forge --file requirements.txt
```

`pip`

```shell
~$ pip install -r requirements.txt
```
`NOTE: to install pyflux`

```shell
~$ git clone https://github.com/RJT1990/pyflux.git
~$ cd pyflux
~$ pip install .
```
After getting the requirements run the below command to watch the data
analysis.

```shell
~$ python anomalous_detection.py
```

If you prefer you can also execute the proyect with this: 
`anomalous_detection.ipynb` Jupyter notebook.

To run a Jupyter Notebook server execute the next comand to start it with the memory constraints (in Mb)
```shell
~$ jupyter notebook --NotebookApp.max_buffer_size=16384
```