import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import jpholiday

df = pd.read_excel("../seino_data/shuuka/20220127_20220630.csv")
df1 = pd.read_excel("../seino_data/shuuka/20210308_20220126.csv")
df2 = pd.read_excel("../seino_data/shuuka/20200101_20210307.csv")
df3 = pd.read_excel("../seino_data/shuuka/20181201_20191231.csv")

shukka = df["出荷日"]
gram = df["重量"]
shukka_day = pd.to_datetime(df['出荷日'],format='%Y%m%d')
gram_day = pd.concat([shukka_day,df['重量']],axis=1)
gram_day = gram_day.set_index(["出荷日"])
gram_day = gram_day.resample('D').sum()
gram_day_graph = gram_day.reset_index(["出荷日"])
# gram_day_graph["出荷日"]
fig, ax= plt.subplots(figsize=(8,4))
ax.set_xlabel("date",fontsize=15)
ax.set_ylabel("weight (kg)",fontsize=15)
ax.bar(gram_day_graph["出荷日"],gram_day_graph['重量'],color="green",width=1)
ax.ticklabel_format(style="sci",  axis="y",scilimits=(0,0))
plt.yticks(fontsize=10)
plt.xticks(fontsize=10)
# plt.ylim(0,2.5e6)
ax.grid()
plt.show()

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
# gram_day_week[gram_day_week["day_name"] == "Sunday"]

fig, ax= plt.subplots(figsize=(8,4))
x1 = gram_day_week[(gram_day_week["day_name"] != "Sunday") & (gram_day_week["day_name"] != "Saturday") 
                  & (gram_day_week["holiday"] == False) & (gram_day_week["出荷日"] != "2022-05-02 00:00:00")]["出荷日"]
y1 = gram_day_week[(gram_day_week["day_name"] != "Sunday") & (gram_day_week["day_name"] != "Saturday") 
                  & (gram_day_week["holiday"] == False) & (gram_day_week["出荷日"] != "2022-05-02 00:00:00")]["重量"]

x = gram_day_week[(gram_day_week["day_name"] == "Saturday") & (gram_day_week["holiday"] == False)]["出荷日"]
y = gram_day_week[(gram_day_week["day_name"] == "Saturday") & (gram_day_week["holiday"] == False)]["重量"]
ax.set_xlabel("date",fontsize=15)
ax.set_ylabel("weight (kg)",fontsize=15)
# ax.bar(x1,y1,color="blue",width=2)
ax.bar(x,y,color="green",width=2)
ax.ticklabel_format(style="sci",  axis="y",scilimits=(0,0))
plt.yticks(fontsize=10)
plt.xticks(fontsize=8)
# plt.xlim(20220501,)
ax.grid()
plt.show()