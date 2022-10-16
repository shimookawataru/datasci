import os
import glob

name_list = ["kansen_chaku", "kansen_hatsu", "shuuka", "haitatsu"]
date_list = ["20220127_20220630", "20210308_20220126", "20200101_20210307", "20181201_20191231"]



path = "../seino_data/" + name_list[3]
files = glob.glob(path + '/*')
# os.rename(files[0],  path + '/' + date_list[0] + ".csv")
# os.rename(files[1],  path + '/' + date_list[2] + ".csv")
# os.rename(files[2],  path + '/' + date_list[1] + ".csv")
# os.rename(files[3],  path + '/' + date_list[3] + ".csv")
    # for j,file in enumerate(files):
    #     os.rename(file,  path + '/' + date_list[j] + ".csv")