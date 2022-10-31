import numpy as np
import pandas as pd
import datetime
import jpholiday
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

df = pd.read_excel("../seino_data/haitatsu/20220127_20220630.csv")
df1 = pd.read_excel("../seino_data/haitatsu/20210308_20220126.csv")
df2 = pd.read_excel("../seino_data/haitatsu/20200101_20210307.csv")
df3 = pd.read_excel("../seino_data/haitatsu/20181201_20191231.csv")

gram = df["重量"]
shukka = df["出荷日"]
shukka_day = pd.to_datetime(df['出荷日'],format='%Y%m%d')
gram_day = pd.concat([shukka_day,df['重量']],axis=1)
gram_day = gram_day.set_index(["出荷日"])
gram_day = gram_day.resample('D').sum()
gram_day_graph = gram_day.reset_index(["出荷日"])

d_name = []
for date in gram_day_graph["出荷日"]:
    d = date.strftime('%A')
    d_name.append(d)

d_name_df = pd.DataFrame(d_name,columns=["day_name"])
holi_name = []
for holi in gram_day_graph["出荷日"]:
    h = jpholiday.is_holiday(holi)
    holi_name.append(h)
holiday_df = pd.DataFrame(holi_name,columns=["holiday"])

gram_day_week = pd.concat([gram_day_graph,d_name_df,holiday_df],axis=1)

gram_day_week[gram_day_week["holiday"] == True]

x_test = gram_day_week[(gram_day_week["出荷日"] >= "2022-06-06 00:00:00") 
                        & (gram_day_week["出荷日"] <= "2022-06-19 00:00:00")
                        &(gram_day_week["day_name"] != "Sunday") 
                        & (gram_day_week["day_name"] != "Saturday")
                        & (gram_day_week["holiday"] == False)]["出荷日"].map(pd.Timestamp.timestamp)
y_test = gram_day_week[(gram_day_week["出荷日"] >= "2022-06-06 00:00:00") 
                        & (gram_day_week["出荷日"] <= "2022-06-19 00:00:00")
                        & (gram_day_week["day_name"] != "Sunday") 
                        & (gram_day_week["day_name"] != "Saturday") 
                        & (gram_day_week["holiday"] == False)]['重量']
x_train = gram_day_week[(gram_day_week["出荷日"] < "2022-06-06 00:00:00")
                        & (gram_day_week["day_name"] != "Sunday") 
                        & (gram_day_week["day_name"] != "Saturday") 
                        & (gram_day_week["holiday"] == False)]["出荷日"].map(pd.Timestamp.timestamp)
y_train = gram_day_week[(gram_day_week["出荷日"] < "2022-06-06 00:00:00")
                        & (gram_day_week["day_name"] != "Sunday") 
                        & (gram_day_week["day_name"] != "Saturday") 
                        & (gram_day_week["holiday"] == False)]['重量']
x_train = x_train.to_numpy().reshape(-1,1)
x_test = x_test.to_numpy().reshape(-1,1)