# Introduction

Actualmente, la cantidad de información que trasita a través del internet es amplia. Con estos grandes volumenes de datos uno de los mejores usos que se les puede dar es la identificación de patrones o anomalías en el tráfico de red aplicado en temas de seguridad. De ahí es que surje la necesidad de utilizar herramientas que nos ayuden al procesamiento de información para observar comportamientos que no se vislumbrar a simple vista. 

En el posterior trabajo, se hará un análisis de dos diferentes archivos que incluyen información sobre el tráfico de red. Ambos archivos son un conjunto de registro recolectados por Zeek IDS, el cual funciona como un analizador de tráfico de red de forma pasiva, además de ser de libre uso. 

Dentro de las actividades que se realizaron se incluyó:

- La conversión de datos crudos a información significativa.
- La búsqueda de paquetes HTTP que no utilizaron puertos convencionales (80 y 8080). 
- Gráficas seccionadas por periódos. 
- Identificación de tipos de ejecutables y explotaciones comúnes. 

Esto con la finalidad de observar información relevante que pudiera ser de ayuda para investigación o mejoras en el negocio. 

# Methodology

De acuerdo a los siguientes dos archivos [conn.log](https://experiencia21.tec.mx/courses/112876/files/42291245/download?download_frd=1) y [http.log](https://experiencia21.tec.mx/courses/112876/files/43820536/download?download_frd=1) se hizo un análisis de sus registros con el fin de obtener información sustancial. 

El primer archivo (`conn.log`) es un compedio de datos con los siguientes atributos: `ts`, `uid`, `id.orig_h`, `id.orig_p`, `id.resp_h`, `id.resp_p`, `proto`, `service`, `duration`, `orig_bytes`, `resp_bytes`, `conn_state`, `local_orig`, `missed_bytes`, `history`, `orig_pkts`, `orig_ip_bytes`, `resp_pkts`, `resp_ip_bytes`, `tunnel_parents`, `threat` y `sample`.

Como este archivo contenía alrededor de 22.6 millones de entradas se limito para únicamente tomar una muestra del 10% lo cual equivaldía a 2.2 millo de entrada para analizar. Consecuentemente, se transformaron los datos a información legible para sus análisis, por ejemplo, la estampa de tiempo y las IPs y puertos únicos de origen. Además, se agruparon el número de conexiones HTTP de acuerdo a su puerto de origen y destino. . 

El segundo archivo (`http.log`) estaba definido de acuerdo a los siguietes atributos:  `ts`, `uid`, `id_orig_h`, `id_orig_p`, `id_resp_h`, `id_resp_p`, `trans_depth`, `method`, `host`, `uri`, `referrer`, `user_agent`, `request_body_len`, `response_body_len`, `status_code`, `status_msg`, `info_code`, `info_msg`, `filename`, `tags`, `username`, `password`, `proxied`, `orig_fuids`, `orig_mime_types`, `resp_fuids`, `resp_mime_types` y `sample`.

En este caso, solamente se filtro la información de los paquetes HTTP que no utilizaban los puertos comúnes y fueron agruparlos por fecha.

Por último, se consultaron todos aquellos paquetes que contuvieran algún tipo de ejecutable o de explotaciones comunes. Y, al igual que los casos pasados, también fueron agrupados por fecha para identificar algunas particularidad. 

# Finds

# Conclusion 