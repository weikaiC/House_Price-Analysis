import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

def getdata(localnum,output_name):
    url ="https://www.sinyi.com.tw/buy/list/Taipei-city/"+localnum+"-zip/Taipei-R-mrtline/03-mrt/default-desc/"
    getpage = requests.get(url+"/index")
    souppage = bs(getpage.text,'lxml')
    page = int(souppage.find_all('li', class_='pageClassName')[-1].text)
    
    result=[]
    for z in range(1,page+1):
        print('page ', z)
        res = requests.get(url+str(1))
        soup = bs(res.text,'lxml')

        for i in range(20):
            table = soup.select('.row')[i]
            title = table.find_all('div','LongInfoCard_Type_Name')[1].text
            address = table.find_all('div','LongInfoCard_Type_Address')[0].find_all('span')[0].text
            house_type = table.find_all('div','LongInfoCard_Type_Address')[0].find_all('span')[2].text
            age = table.find_all('div','LongInfoCard_Type_Address')[0].find_all('span')[1].text.replace('--','0').replace('年','')
            structure = table.find_all('div','LongInfoCard_Type_HouseInfo')[0].find_all('span')
            area = structure[0].text.replace('建坪','').replace('地坪','')
            price = soup.find_all('span',style='font-size:1.75em;font-weight:500;color:#dd2525')[i].text.replace(',','')

            s = structure[2].text
            if ('房' in s) & ('廳' in s) & ('衛' in s):
                room=s.split('房')[0]
                hall=s.split('房')[1].split('廳')[0]
                bathroom=s.split('房')[1].split('廳')[1].split('衛')[0]
            elif ('房' in s) & ('廳' in s):
                room=s.split('房')[0]
                hall=s.split('房')[1].split('廳')[0]
                bathroom='0'
            elif ('廳' in s) & ('衛' in s):
                room='0'
                hall=s.split('廳')[0]
                bathroom=s.split('廳')[1].split('衛')[0]
            elif ('房' in s) & ('衛' in s):
                room=s.split('房')[0]
                hall='0'
                bathroom=s.split('房')[1].split('衛')[0]
            elif '房' in s:
                room=s.split('房')[0]
                hall='0'
                bathroom='0'
            elif '廳' in s:
                room='0'
                hall=s.split('廳')[0]
                bathroom='0'
            elif '衛' in s:
                room='0'
                hall='0'
                bathroom=s.split('衛')[0]
            else:
                print(s)

            if "-" in structure[3].text.split('/')[0]:
                floor=structure[3].text.split('/')[0].split('-')[1].replace('樓','')
            else:
                floor=structure[3].text.split('/')[0].replace('樓','')

            total_floor=structure[3].text.split('/')[1].replace('樓','')
            perprice = round(int(price) / float(area), 2) 

            temp = [title, address, house_type, age, area, price, room, hall, bathroom, floor, total_floor, perprice]
            result.append(temp)

    data = pd.DataFrame(result, columns=['title', 'address', 'house_type', 'age', 'area', 'price', 'room', 'hall', 
                                     'bathroom', 'floor', 'total_floor', 'perprice'])
    data.to_csv(output_name+".csv",encoding='utf-8')

getdata('106','信義房屋大安')
getdata('110','信義房屋信義')
getdata('116','信義房屋文山')