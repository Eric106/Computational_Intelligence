from pandas import DataFrame, read_parquet, read_csv
from datetime import datetime as dt
from pprint import pprint
from data_utils import split_train_test

# LOAD DATA FROM LOG FILE AND SAVE TO PARQUET FILE TO IMPROVE PERFORMANCE AT READING THE DATA

# log_col_names = ["ts", "uid", "id_orig_h", "id_orig_p", "id_resp_h", "id_resp_p", "proto", "service", "duration", "orig_bytes", "resp_bytes",
#                    "conn_state", "local_orig", "missed_bytes", "history", "orig_pkts", "orig_ip_bytes", "resp_pkts", "resp_ip_bytes", "tunnel_parents"]
# df = read_csv("conn.log",sep="\t",header=None,names=log_col_names,low_memory=False)

# df.to_parquet("conn.parquet",index=False)
# trainSet, test_set = split_train_test(df,0.1)
# del trainSet
# test_set.to_parquet("conn_sample.parquet",index=False)
# exit()

#---------------------------------------------------------------------------------------------
# df = read_parquet("conn.parquet")
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