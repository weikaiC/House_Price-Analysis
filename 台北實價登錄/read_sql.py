import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://root:dv102@localhost:3306/house')

sql_cmd = 'select * From housesell'

df = pd.read_sql(sql=sql_cmd, con=engine)

df.to_csv('house_sell.csv',encoding='utf-8-sig')

