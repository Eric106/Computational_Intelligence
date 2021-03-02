from pandas import DataFrame, read_parquet, read_csv
from datetime import datetime as dt
from pprint import pprint
from time import sleep, time
import numpy as np
import sys

def get_random_sample_data(data:DataFrame, test_ratio:float=0.1):
    ''' permutation: Randomly permute a sequence or return a permuted range (ndarray).
                    If x is a multi-dimensional array, it is only shuffled along its first index.'''
    shuffled_indices = np.random.permutation(len(data))
    test_set_size = int(len(data) * test_ratio)
    test_indices = shuffled_indices[:test_set_size] #return the “x-first” values
    return data.iloc[test_indices]


def log_to_parquet(path_file: str, file_cols=list):
    # LOAD DATA FROM A LOG FILE AND SAVE IT ON A PARQUET FILE TO IMPROVE PERFORMANCE AT READING THE DATA
    file_name = path_file.split('.log')[0]+'.parquet'
    df = read_csv(path_file, sep="\t", header=None,
                    names=file_cols, low_memory=False)
    df.to_parquet(file_name, index=False)
    return file_name
        

#---------------------------------------------------------------------------------------------

def conn_analysis():
    # log_col_names = ["ts", "uid", "id_orig_h", "id_orig_p", "id_resp_h", "id_resp_p", "proto", "service", "duration", "orig_bytes", "resp_bytes",
    #                     "conn_state", "local_orig", "missed_bytes", "history", "orig_pkts", "orig_ip_bytes", "resp_pkts", "resp_ip_bytes", "tunnel_parents"]

    # parquet_file = log_to_parquet(path_file="conn.log",file_cols=log_col_names)
    # complete_df = read_parquet(parquet_file)

    # complete_df = read_parquet("conn.parquet")
    # sample_df = get_random_sample_data(complete_df)

    # sample_df.to_parquet("conn_sample.parquet",index=False)
    
    # df = sample_df

    df = read_parquet("conn_sample.parquet")

    df["ts"] = df["ts"].astype("float")
    df["ts"] = list(map(lambda date: dt.fromtimestamp(date), df["ts"].tolist()))
    df["duration"] = list(map(lambda dur: float(dur) if not "-" in dur else 0.0, df["duration"].tolist()))
    print(df.info())


    important_cols = ["ts","id_orig_h", "id_resp_p", "duration"]

    df_not_web_port = df[(df["id_resp_p"]!=80) & (df["id_resp_p"]!=8080)].copy()
    df_not_web_port.reset_index(drop=True,inplace=True)

    print('\n',"Not http ports: ")
    pprint(df_not_web_port[important_cols])

    df_gp_not_web_port = df_not_web_port.groupby(important_cols[1:3]).size().to_frame().reset_index()
    df_gp_not_web_port.rename(columns={0:"count"},inplace=True)
    df_gp_not_web_port.sort_values(by="count",ascending=False,inplace=True)


    print('\n',"Not http ports groupby: ")
    pprint(df_gp_not_web_port)


    df_long_conn = df[df["duration"]>5].copy()
    df_long_conn.sort_values(by="duration",ascending=False,inplace=True)
    df_long_conn.reset_index(drop=True,inplace=True)
    print('\n',"Long duration connections: ")
    pprint(df_long_conn[important_cols])

def main():
    intiTime = time()

    conn_analysis()
        
    elapsedTime = round(time()-intiTime, 2)
    elapsedTime = str(elapsedTime/60) + "m" if elapsedTime >= 60 else str(elapsedTime)+"s"
    print("\nTiempo del proceso --->", elapsedTime)
    sys.exit()

main()
