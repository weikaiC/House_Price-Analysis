#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
from bs4 import BeautifulSoup as bs
import requests
from lxml import html
get_ipython().system('pip install pymysql')
get_ipython().system('pip install sqlalchemy')


# In[8]:


title = []
address = []
type = []
age = []
large = []
price = []
room = []
hall = []
bathroom = []
floor = []
total_floor = []
page = 1
while page < 2:
    url = 'https://www.twcd.com.tw/object_listS.php'
    curSession = requests.Session() 
    payload = { 'typeV': 1,
    'np': page,
    'so': 0,
    'tp': 'def',
    'vr': 0, 
    'City': 1,
    'town[]': 116,#郵遞區號 信義區:110,文山區:116,大安區:106
    'money1': 0,
    'area1': 0,
    'year1': 0,
    'year2': 0,
    'floor1': 0,
    'floor2': 0,
    'Parking[]': -1}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'}

    res = curSession.post(url,data=payload, headers=headers)
    res = curSession.post(url,data=payload, headers=headers)
    page += 1
    tree = html.fromstring(res.json()[0])
    soup = bs(res.json()[0],'lxml')
    ti = soup.select('.OBJNAMEa')
    for t in ti:
        title.append(t.text)
    for add in tree.xpath("//td[2]/div[2]/text()"):
        address.append(add.replace('\xa0\xa0',''))
    for tp in tree.xpath("//td[2]/div[3]/div[1]/text()"):
        type.append(tp)
    for ag in tree.xpath("//tr/td[2]/div[4]/div[1]/text()"):
        age.append(ag.replace('年',''))
    for rt in tree.xpath("//tr/td[2]/div[3]/div[2]/text()"):
        room.append(rt[0:2].replace('房',''))
    for hl in tree.xpath("//tr/td[2]/div[3]/div[2]/text()"):
        hall.append(hl[2:4].replace('廳','').replace('房',''))
    for bat in tree.xpath("//tr/td[2]/div[3]/div[2]/text()"):
        bathroom.append(bat[4:7].replace('廳','').replace('衛',''))
    for fl in tree.xpath("//tr/td[2]/div[3]/div[3]/text()"):
        floor.append(fl[0:2].replace('/',''))
    for tf in tree.xpath("//tr/td[2]/div[3]/div[3]/text()"):
        total_floor.append(tf[2:12].replace('/',''))
    for ar in tree.xpath("//tr/td[2]/div[4]/div[3]/text()"):
        large.append(ar.replace('\xa0\xa0','').replace('坪',''))
    for p in tree.xpath('//tr/td[2]/div[5]/div/text()'):
           if p.replace('\t','').replace('\n','') != '':
                price.append(p)
perprice = [int(a) / float(b) for a, b in zip(price, large)]


# In[9]:


import numpy as np
import pandas as pd
dic = {}
dic['title']=title
dic['address']=address
dic['house_type']=type
dic['age']=age
dic['area']=large
dic['price']=price
dic['perprice']=np.round(perprice, decimals=1)
dic['room']=room
dic['hall']=hall
dic['bathroom']=bathroom
dic['floor']=floor
dic['total_floor']=total_floor
data = pd.DataFrame(dic)


# In[5]:


from sqlalchemy import create_engine
# 初始化資料庫連線，使用pymysql模組
# MySQL的使用者：root, 密碼:dv102, 埠：3306,資料庫：world
engine = create_engine('mysql+pymysql://admin:dv102dv102@database-1.cb5frtthut3g.us-west-1.rds.amazonaws.com:3306/Housesell')
# 將新建的DataFrame儲存為MySQL中的資料表，不儲存index列
data.to_sql('Housesell', engine, if_exists='append', index= False)
print('Read from and write to Mysql table successfully!')


# In[ ]:




