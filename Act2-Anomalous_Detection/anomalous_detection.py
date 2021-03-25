from time import time
from os import listdir
from pandas import read_parquet, read_csv, DataFrame
from datetime import datetime as dt

def log_to_parquet(in_file: str, out_file: str, file_cols: list, parquet_engine: str):
    # LOAD DATA FROM A LOG FILE AND SAVE IT ON A PARQUET FILE TO IMPROVE PERFORMANCE AT READING THE DATA
    df = read_csv(in_file, sep="\t", header=None,
                  names=file_cols, low_memory=False)
    df.to_parquet(out_file, index=False, engine=parquet_engine)
    del df


def get_files_inFolder(folder: str, fileType: str):
    return list(filter(lambda fileName: 
                            fileName[-len(fileType):] == fileType,
                        listdir(folder)))

def slice_dataFrame(dataFrame: DataFrame, percent_slice: float):
    total_data


def an_detect(http_log_name: str):
    P_ENGINE = "pyarrow"
    cols_log = ['ts', 'uid', 'id_orig_h', 'id_orig_p', 'id_resp_h', 'id_resp_p',
                'trans_depth', 'method', 'host', 'uri', 'referrer', 'user_agent',
                'request_body_len', 'response_body_len', 'status_code', 'status_msg',
                'info_code', 'info_msg', 'filename', 'tags', 'username',
                'password', 'proxied', 'orig_fuids', 'orig_mime_types', 'resp_fuids',
                'resp_mime_types']
    list_parq_files = get_files_inFolder("./","parq")
    http_parq_name = (http_log_name.split('.')[0])+".parq"
    if not http_parq_name in list_parq_files:
        log_to_parquet(http_log_name, http_parq_name, cols_log, P_ENGINE)
    
    important_cols = ["ts","id_orig_h", "id_resp_p","response_body_len"]
    df = read_parquet(http_parq_name, columns=important_cols)
    df["ts"] = list(map(
                    lambda date: 
                        dt.fromtimestamp(float(date)),
                    df["ts"].tolist()))
    print(df.info())
    print(df)


def main():
    paths = {
        "http":"http-1.log"
    }

    intiTime = time()

    an_detect(http_log_name=paths["http"])

    elapsedTime = round(time()-intiTime, 2)
    elapsedTime = str(elapsedTime/60) + \
        "m" if elapsedTime >= 60 else str(elapsedTime)+"s"
    print("\nTiempo del proceso --->", elapsedTime)


main()