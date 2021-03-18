# Introduction

Actualmente, la cantidad de información que trasita a través del internet es amplia. Con estos grandes volumenes de datos uno de los mejores usos que se les puede dar es la identificación de patrones o anomalías en el tráfico de red aplicado en temas de seguridad. De ahí es que surje la necesidad de utilizar herramientas que nos ayuden al procesamiento de información para observar comportamientos que no se vislumbrar a simple vista. 

Currently, the amount of information that transit through the Internet is wide.With these large data volumes one of the best uses that can be given is the identification of patterns or anomalies in the network traffic applied in safety issues.From there, it is that the need to use tools that help us from the information processing to observe behaviors that will not be glimpsed at first glance.

En el posterior trabajo, se hará un análisis de dos diferentes archivos que incluyen información sobre el tráfico de red. Ambos archivos son un conjunto de registro recolectados por Zeek IDS, el cual funciona como un analizador de tráfico de red de forma pasiva, además de ser de libre uso. 

In the subsequent work, an analysis of two different files that include information on network traffic will be made.Both files are a set of record collected by Zeek IDS, which works as a network traffic analyzer in a passive way, as well as free use.

Dentro de las actividades que se realizaron se incluyó:

Within the activities that were carried out, it was included:

- La conversión de datos crudos a información significativa.

- The conversion of raw data to significant information.
- La búsqueda de paquetes HTTP que no utilizaron puertos convencionales (80 y 8080). 

- The search for HTTP packets that did not use conventional ports (80 and 8080).
- Gráficas seccionadas por periódos. 

- Graphs sectioned by peri�s.
- Identificación de tipos de ejecutables y explotaciones comúnes. 

- Identification of types of executables and common holdings.

Esto con la finalidad de observar información relevante que pudiera ser de ayuda para investigación o mejoras en el negocio. 

This with the purpose of observing relevant information that could be helpful for research or improvements in the business.

# Methodology

El análisis se hizo de acuerdo a los siguientes dos archivos [conn.log](https://experiencia21.tec.mx/courses/112876/files/42291245/download?download_frd=1) y [http.log](https://experiencia21.tec.mx/courses/112876/files/43820536/download?download_frd=1).

The analysis was made according to the following two files [conn.log](https://experience21.tec.mx/courses/112876/files/42291245/download?download_frd=1) and [HTTP.LOG](https://experience21.tec.mx/courses/112876/files/43820536/download?download_frd=1).

El primer archivo (`conn.log`) es un compedio de datos con los siguientes atributos: `ts`, `uid`, `id.orig_h`, `id.orig_p`, `id.resp_h`, `id.resp_p`, `proto`, `service`, `duration`, `orig_bytes`, `resp_bytes`, `conn_state`, `local_orig`, `missed_bytes`, `history`, `orig_pkts`, `orig_ip_bytes`, `resp_pkts`, `resp_ip_bytes`, `tunnel_parents`, `threat` y `sample`.

Como este archivo contenía alrededor de 22.6 millones de entradas se limito para tomar únicamente una muestra del 10%, lo cual equivaldría a 2.2 millones de entradas para analizar. Asimismo, los archivos fueron transformados al formato binario parquet. Disminuyendo el tiempo de ejecución y el uso en memoria. 

As this file contained around 22.6 million inputs, it is limited to only take a sample of 10%, which would be equivalent to 2.2 million tickets to analyze.Likewise, the files were transformed to the binary parquet format.Decreasing the execution time and use in memory.

En el siguiente código se pueden observar diferentes aspectos que describen la forma en que se manipulo el conjunto de datos: 

In the next code you can observe different aspects that describe the way in which the data set is manipulated:

```python
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 2269436 entries, 0 to 2269435
Data columns (total 3 columns):
 #   Column     Dtype         
---  ------     -----         
 0   ts         datetime64[ns]
 1   id_orig_h  object        
 2   id_resp_p  int64         
dtypes: datetime64[ns](1), int64(1), object(1)
memory usage: 51.9+ MB
None
```

- La cantidad exacta de entradas fueron 2269436.

- The exact amount of tickets was 2269436.
- Únicamente se tomarón tres columnas de los atributos totales (`ts`, `id.orig_p`, `id.resp_p`). 

- Only three columns of the total attributes (`ts`,` id.orig_p`, `id.resp_p`).
- La estampa de tiempo fue manipulada a otro tipo de objeto para desempeñar series-time analysis.

- The time stamp was manipulated to another type of object for performing series-time analysis.

En la siguiente impresión se muestran las veces que se contaron la IP de origen correspondiente 

The following impression shows the times that the corresponding IP was counted
a un puerto. 

to a port.

```python
 different ports to 80: 
                                               count
id_orig_h                           id_resp_p       
192.168.204.45                      443         4865
2001:dbb:c18:202:20c:29ff:fe18:b667 445         4840
192.168.202.110                     443         3973
192.168.202.140                     443         3664
192.168.202.108                     443         3447
...                                              ...
192.168.202.110                     48469          1
                                    48479          1
                                    48481          1
                                    48529          1
192.168.202.79                      35803          1

[266880 rows x 1 columns]
```

El segundo archivo (`http.log`) definido de acuerdo a los siguietes atributos:  `ts`, `uid`, `id_orig_h`, `id_orig_p`, `id_resp_h`, `id_resp_p`, `trans_depth`, `method`, `host`, `uri`, `referrer`, `user_agent`, `request_body_len`, `response_body_len`, `status_code`, `status_msg`, `info_code`, `info_msg`, `filename`, `tags`, `username`, `password`, `proxied`, `orig_fuids`, `orig_mime_types`, `resp_fuids`, `resp_mime_types` y `sample`; fue filtrado para que solo se mostraran los campos relevantes conforme a la siguiente impresión: 

The second file (`HTTP.LOG`) Defined according to the following attributes:` TS`, `Uid`,` ID_ORIG_H`, `ID_ORIG_P`,` ID_RESP_H`, `ID_RESP_P`,` trans_depth`, `Method``Host`,` Uri`, `Referrer`,` user_agent`, `request_body_len`,` response_body_len`, `status_code`,` status_msg`, `info_code`,` info_msg`, `filename`,` tags`, `username`,` Password`, `Proxied`,` orig_fuids`, `orig_mime_types`,` resp_fuids`, `resp_mime_types` and` sample`;It was filtered so that only the relevant fields according to the following impression will be shown:

```python
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 807537 entries, 0 to 807536
Data columns (total 4 columns):
 #   Column           Non-Null Count   Dtype         
---  ------           --------------   -----         
 0   ts               807537 non-null  datetime64[ns]
 1   id_orig_h        807537 non-null  object        
 2   id_resp_p        807537 non-null  int64         
 3   resp_mime_types  807537 non-null  object        
dtypes: datetime64[ns](1), int64(1), object(2)
memory usage: 24.6+ MB
None
```

Al igual que en el caso anterior el uso en memoria es considerablemente bajo, además de que se tomaron solo cuatro columnas de los poco más de 28 atributos que contiene cada entrada de la bitacóra. 

As in the previous case, the use in memory is considerably low, in addition to that only four columns of the little more than 28 attributes containing each entry of the bitacole were taken.

La excepción en esta parte del análisis fue que se decidió analizar todo aquellos puertos diferentes al 80 y 8080; y conocer los tipos de ejecutable y explotaciones comúnes de acuerdo 

The exception in this part of the analysis was that it was decided to analyze all those ports different from 80 and 8080;and know the types of executable and common holdings agree

```python
Different ports to 80 and 8080: 
                                 id_orig_h  id_resp_p        resp_mime_types
ts                                                                          
2011-07-30 09:38:13.349379   192.168.68.10         81              text/html
2011-08-13 16:31:10.361867    192.168.1.10         81              image/gif
2011-08-15 22:17:34.542855   192.168.36.10         81              image/gif
2011-08-16 07:15:15.135895  192.168.119.10         81              text/html
2011-08-28 05:38:14.486610  192.168.119.10         81              image/gif
...                                    ...        ...                    ...
2014-07-14 02:25:35.649867   192.168.67.10      19910  application/x-dosexec
2014-07-14 02:25:49.922045   192.168.67.10      19910              text/html
2014-07-14 02:25:50.045418   192.168.67.10      19910              text/html
2014-07-14 02:25:50.231042   192.168.67.10      19910              text/html
2014-07-14 02:25:50.240084   192.168.67.10      19910              text/html
```

La siguiente gráfica ejemplifica como fue seccionada los datos de la impresión anterior. 

The following graph exemplifies how the data of the previous printing was sectioned.

![alt text](./images/no80_8080.png)

Por último, los datos fueron segmentados de acuerdo a la siguiente impresión para generar una gráfica mostrando cada cuarto los tipos de ejcución y explotaciónes comunes conforme a la IP de origin junto con el puerto. 

Finally, the data were segmented according to the following impression to generate a graph showing each fourth reasons for common hunting and exploitation according to the origin IP along with the port.

```python
Exploit Types: ['application/x-java-applet', 'application/pdf', 'application/zip', 'application/jar', 'application/x-shockwave-flash']
Executable Types: ['application/x-dosexec', 'application/octet-stream', 'binary', 'application/vnd.ms-cab-compressed']
                                id_orig_h  id_resp_p  \
ts                                                     
2011-07-22 17:08:11.247202  192.168.95.10         80   
2011-07-22 17:08:14.015447  192.168.95.10         80   
2011-07-22 17:08:23.140325  192.168.95.10         80   
2011-07-22 17:08:49.264341  192.168.95.10         80   
2011-07-22 17:08:49.378921  192.168.95.10         80   
...                                   ...        ...   
2014-07-14 08:44:05.730220  192.168.29.10         80   
2014-07-14 08:44:06.603410  192.168.29.10         80   
2014-07-14 08:44:06.677585  192.168.29.10         80   
2014-07-14 08:44:06.687420  192.168.29.10         80   
2014-07-14 08:44:11.976348  192.168.29.10         80   

                                      resp_mime_types  
ts                                                     
2011-07-22 17:08:11.247202      application/x-dosexec  
2011-07-22 17:08:14.015447            application/pdf  
2011-07-22 17:08:23.140325      application/x-dosexec  
2011-07-22 17:08:49.264341  application/x-java-applet  
2011-07-22 17:08:49.378921            application/zip  
...                                               ...  
2014-07-14 08:44:05.730220                     binary  
2014-07-14 08:44:06.603410                     binary  
2014-07-14 08:44:06.677585                     binary  
2014-07-14 08:44:06.687420                     binary  
2014-07-14 08:44:11.976348      application/x-dosexec 
```

![alt text](./images/exploits_types.png)

# Finds

```python
 different ports to 80: 
                                               count
id_orig_h                           id_resp_p       
192.168.204.45                      443         4865
2001:dbb:c18:202:20c:29ff:fe18:b667 445         4840
```

En la primera sección al obtener todas IPs de origin y los puertos diferentes a 80 del archivo `conn.log` podemos notar que la mayoría de los ingresos fueron mediante HTTPS (puerto 443), pero hay que nota otra dato importante que el segundo puerto mayormente consultado fue el 445. 

In the first section when obtaining all origin IPS and the ports other than 80 of the "conn.log file, we can notice that most income were through HTTPS (port 443), but it is worth another important fact that the second portMostly consulted was 445.

El puerto 445 es utilizado para el protocolo `Server Message Block (SMB)`. El protocolo permite compartir información entre archivos, impresoras, entre otras sobre sistemas Wndows. Sin embargo, también es un acceso abierto a dos tipos de gusanos: `Sasser` y `Nimda`. 

Port 445 is used for the `Server Message Block (SMB) protocol.The protocol allows sharing information between files, printers, among others on Wndows systems.However, it is also an open access to two types of worms: `Sasser` and` Nimda`.

`Sasser` funciona escaneando un rango de direcciones IP y explotando vulnerabilidad a través del puerto 445. Su principal función es desbordamiento de buffer en un componente clave conocido como `LSASS (Local Security Authority Subsystem Service)` dentro de los sistemas `Windows`. 

`Sasser` works scanning a range of IP addresses and exploiting vulnerability through port 445. Its main function is buffer overflow on a key component known as` LSASS (Local Security Authority Subsystem Service )``

Por otro lado, `Nimda` tiene el propósito de extender su infección a otros ficheros de la computadora o a otros dispositivos con el mismo sistema (`Windows`) conectados a la red. 

On the other hand, `Nimda` has the purpose of extending its infection to other computer files or other devices with the same system (` Windows`) connected to the network.

Ambos gusano pueden ser fácilmente eliminados configurando el firewall para evitar el tráfico a través del puerto 445. 

Both worm can be easily eliminated by configuring the firewall to avoid traffic through port 445.

```python
Different ports to 80 and 8080: 
                                 id_orig_h  id_resp_p        resp_mime_types
ts                                                                      
2014-07-14 02:25:35.649867   192.168.67.10      19910  application/x-dosexec
2014-07-14 02:25:49.922045   192.168.67.10      19910              text/html
```

Tomando de referencia la impresión anterior uno de los tipos de aplicaciones es ejecutable utilizando el puerto 19910, des lo cuales no se tiene asignado ningún tipo de detalle. Posiblemente, alguno de los dos gusanos informaticos anteriormente mencionados ejecutaron aplicaciones ejecutable en `Windows` mediante el puerto 19910. 

Taking reference the previous impression One of the types of applications is executable using the port 19910, what is not assigned any detail type.Possibly, some of the aforementioned two computer worms executed executable applications in `Windows` through the port 19910.

Por otra parte, se puede también hacer un análisis de la información gráficada.

On the other hand, an analysis of the graphic information can also be done.

![alt text](./images/no80_8080.png)

Por ejemplo, en esta primera gráfica se muestra la cantidad de veces que se ingreso mediante una IP y puerto de origen. A simple vista podemos notar que los datos cambian de acuerdo al año y trimestre. Durante 2012 y 2013 los datos demuestra que hubo gran actividad en cuanto a conexiones, aunque fue segundo trimestre en 2012, último trimestre del 2012, y principio del 2013 en el primer trimestre donde hubo una gran cantidad de entradas. Marcando el primer trimestre del 2013 como el más alto en registros.

For example, in this first graph the amount of times is shown by an IP and source port.At first glance we can see that the data changes according to the year and quarter.During 2012 and 2013 the data shows that there was great activity in terms of connections, although it was a second quarter in 2012, last quarter of 2012, and beginning of 2013 in the first quarter where there was a lot of tickets.Marking the first quarter of 2013 as the highest in records.

![alt text](./images/exploits_types.png)

Esta gráfica al igual que la anterior representa el número de tipos de ataque y explotaciones comúnes que se registraron cada trimestre. Incluso resalta que durante el segundo trimestre de 2012 hubo una cantidad fuerte de registros, superando por mucho los datos recuperados en otros trimestres. 

This graphic as well as the above represents the number of attack types and common farms that were recorded each trimester.It even emphasizes that during the second quarter of 2012 there was a strong number of records, far exceeding the data recovered in other quarters.

Al observar dichas gráficas podríamos reforzar la idea de que fue probable que durante ese tiempo fue cuando se exploto la vulnerabilidad del sistema al inyectar una gran cantidad de archivos ejecutable sobre los cuales pudo estar trabajando alguno tipo de gusano. 

By observing these graphics, we could reinforce the idea that it was likely that during that time it was when the vulnerability of the system was exploited by injecting a large amount of executable files on which any type of worm could be working.

# Conclusion 

Al realizar el análisis de estos dos archivos (`conn.log` y `http.log`) se logró identificar que posiblemente el sistema del cual se extranjeron dichas bitácoras pude haber sufrido una explotación al haber identificado un vulnerabilidad dentro de sus sistemas. No obstante, dicha patrón no pudo haber sido encontrado sin la correcta manipulación e interpretación de los datos. 

When performing the analysis of these two files (`conn.log` and` http.log`) it was possible to identify that possibly the system of which such bits were alienated could have suffered an exploitation having identified a vulnerability withinYour systems.However, this patron could not have been found without the correct manipulation and interpretation of the data.

Si bien es una vulnerabilidad que pude haber causado problemas importantes, herramientas como los antivirus, firewalls o protocolos para manejo de amanzas son aspectos suficientes para cesar el intento de querer explotar una sección vulnerable del sistema. 

While it is a vulnerability that could have caused important problems, tools such as antivirus, firewalls or amazing management protocols are sufficient aspects to cease the attempt to exploit a vulnerable system section.

Finalmente, realizar este tipo de ejercicios periódicamente en la infraestructura de red ayudaría a monitorear amenazas latentes con estas características. Incluso, se podría automatizar la lectura de dichos `logs` y su interpretación mediante valores de entrada y acciones que requerieren un proceso fijo del cual solo dependen un par de variables.
Finally, performing this type of exercises peri�dically in the network infrastructure would help monitor latent threats with these features.Even, the reading of said `logs` and its interpretation could be automated through entry values and actions that require a fixed process from which only a pair of variables depend.