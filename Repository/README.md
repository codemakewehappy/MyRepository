创建的Python Django Web框架


-- coding: UTF-8 --
import os
import pandas as pd
import csv

def pandas_csv_read():
readline = csv.reader(open("C:\Users\pawnshop_NO.8\Desktop\test\panda-import.csv", "r"))
data = {}
line_num = 0
for line in readline:
line_num += 1
if line_num != 1:
collectTime = line[0]
mergerSendTime = line[1]
mergerWorkId = line[2]
motId = line[3]
tableName = line[4]
dataTableSize = line[5]
key = collectTime
if not data.has_key(key):
collecttime_data = {}
collect_time = []
merger_send_time = []
mergerwork_Id = []
mot_Id = []
table_Name = []
data_table_size = []
collect_time.append(collectTime)
merger_send_time.append(mergerSendTime)
mergerwork_Id.append(mergerWorkId)
mot_Id.append(motId)
table_Name.append(tableName)
data_table_size.append(dataTableSize)
collecttime_data['collectTime'] = collect_time
collecttime_data['mergerSendTime'] = merger_send_time
collecttime_data['mergerWorkId'] = mergerwork_Id
collecttime_data['motId'] = mot_Id
collecttime_data['tableName'] = table_Name
collecttime_data['dataTableSize'] = data_table_size
data[key] = collecttime_data
else:
update_collecttime_data = data.get(key)
update_collecttime_data['collectTime'].append(collectTime)
update_collecttime_data['mergerSendTime'].append(mergerSendTime)
update_collecttime_data['mergerWorkId'].append(mergerWorkId)
update_collecttime_data['motId'].append(motId)
update_collecttime_data['tableName'].append(tableName)
update_collecttime_data['dataTableSize'].append(dataTableSize)
pandas_write_csv("C:\Users\pawnshop_NO.8\Desktop\test\", data)

def pandas_write_csv(filePath, dataContents):
sorted(dataContents.keys())
for key in dataContents.iterkeys():
new_filepath = filePath + key[0:10]
import_data = pd.DataFrame(dataContents.get(key))
if not os.path.exists(new_filepath):
os.mkdir(new_filepath)

    if not os.path.exists(new_filepath + "\\datfile-" + key + ".csv"):
        file = open(new_filepath + "\\datfile-" + key + ".csv")
        import_data.to_csv(file, index=None)
    else:
        # 比较import_data 和old_data 数据，将多余的import_data数据追加到csv中
        old_data = csv.reader(open(new_filepath + "\\datfile-" + key + ".csv", "r"))
        need_import_data = construct_data(old_data, import_data)
        need_import_data_pd=pd.DataFrame(need_import_data)
        file = open(new_filepath + "\\datfile-" + key + ".csv","a")
        need_import_data_pd.to_csv(file, index=None)
def construct_data(old_data, new_data):
line_num = 0
construct_old_data = set()
construct_new_data = set()
old_title = []
for line in old_data:
line_num += 1
if line_num == 1:
old_title = list(line)
else:
key_str = ''
for key_index in range(len(old_title)):
key_str += line[key_index] + '*'
construct_old_data.add(key_str)

collectTime = new_data.get('collectTime')
for i in range(len(collectTime)):
    key_str = ''
    for key_title in old_title:
        key_str += new_data.get(key_title)[i] + '*'
    construct_new_data.add(key_str)

need_import_data = construct_new_data - construct_old_data

need_import_data_dict={}
if len(need_import_data) != 0:
    for str in need_import_data:
        str_data=str.split("*")
        for i in range(len(old_title)):
            if not need_import_data_dict.has_key(old_title[i]):
                data_list=[]
                data_list.append(str_data[i])
                need_import_data_dict[old_title[i]]=data_list
            else:
                need_import_data_dict.get(old_title[i]).append(str_data[i])

return need_import_data_dict
if name == 'main':
pandas_csv_read()
