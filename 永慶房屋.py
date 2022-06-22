from email import header
import requests
from bs4 import BeautifulSoup as bs
from selenium.webdriver.chrome.options import Options 
from lxml import html
from lxml import cssselect
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

#pip install -r requirements.txt

def update_to_SQL(district_name):  #ex:'大安區'
    tit_lis = []
    add_lis = []
    type_lis = []
    age_lis = []
    area_lis = []
    room_lis = []
    price_lis = []
    floor_lis = []
    url = 'https://buy.yungching.com.tw/region/%E5%8F%B0%E5%8C%97%E5%B8%82-'+district_name+'_c/_rm/?pg='
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'}

    for page in range(1, 31):
        res = requests.get(url+str(page), headers=headers)
        soup = bs(res.text,'lxml')
        for i in soup.find_all('h3'):
            tit_lis.append(i.text)
        for i in soup.select('.item-description span'):
            add_lis.append(i.text)
        for i in soup.select('.item-info-detail li:nth-child(1)'):
            type_lis.append(i.text)
        for i in soup.select('.item-info-detail li:nth-child(2)'):
            age_lis.append(i.text.replace('\r\n','').replace('年            ',''))
        for i in soup.select('.item-info-detail li:nth-child(6)'):
            area_lis.append(i.text.replace('建物','').replace('坪',''))
        for i in soup.select('.item-info-detail li:nth-child(7)'):
            room_lis.append(i.text.replace('房(室)',',').replace('廳',',').replace('衛            ','').replace('\r\n',''))
        for i in soup.select('.price-num'):
            price_lis.append(i.text.replace(',',''))
        for i in soup.select('.item-info-detail li:nth-child(3)'):
            floor_lis.append(i.text.replace('樓            ','').replace('\r\n ',''))

    d = {}
    d['title'] = tit_lis
    d['address'] = add_lis
    d['house_type'] = type_lis
    d['age'] = age_lis
    d['area'] = area_lis
    d['room0'] = room_lis
    d['price'] = price_lis
    d['floor0'] = floor_lis

    df = pd.DataFrame(d)
    df['price'] = pd.to_numeric(df['price'])
    df['area'] = pd.to_numeric(df['area'])
    df['perprice'] = df['price'] / df['area']
    df['perprice'] = round(df['perprice'], 2)

    spl = df['room0'].str.split(',', expand=True)
    spl = spl.stack()
    df['room'] = (spl[:,0])
    df['hall'] = (spl[:,1])
    df['bathroom'] = (spl[:,2])


    spl2 = df['floor0'].str.split(' ~ ', expand=True)
    spl2 = spl2.stack()
    df['floor1'] = (spl2[:,1])
    spl3 = df['floor1'].str.split(' / ', expand=True)
    spl3 = spl3.stack()
    df['floor'] = (spl3[:,0])
    df['total_floor'] = (spl3[:,1])
    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    result_df = df.drop(['room0', 'floor0', 'floor1'], axis=1)
    
    # result_df.to_csv(district_name+'.csv',encoding="utf_8_sig") #若需要做本地備份

    conn = create_engine('mysql+pymysql://admin:dv102dv102@database-1.cb5frtthut3g.us-west-1.rds.amazonaws.com:3306/Housesell', pool_pre_ping=True, encoding='utf8')
    result_df.to_sql("Housesell", conn, if_exists='append', index = False)

update_to_SQL('大安區')
update_to_SQL('信義區')
update_to_SQL('文山區')