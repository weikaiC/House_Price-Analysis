import os
import pandas as pd
from matplotlib import pyplot as plt

# 歷年資料夾
dirs = [d for d in os.listdir() if d[:4] == 'real']

dfs = []

for d in dirs:
    print(d)
    df = pd.read_csv(os.path.join(d,'a_lvr_land_a.csv'), index_col=False)
    df['Q'] = d[-1]
    dfs.append(df.iloc[1:])
    
df = pd.concat(dfs, sort=True)

# 新增交易年份
df['year'] = df['交易年月日'].str[:-4].astype(int) + 1911



# 平方公尺換成坪
df['單價元平方公尺'] = df['單價元平方公尺'].astype(float)
df['單價元坪'] = df['單價元平方公尺'] * 3.30579

# 建物型態
df['建物型態2'] = df['建物型態'].str.split('(').str[0]

# 刪除有備註之交易（多為親友交易、價格不正常之交易）
df = df[df['備註'].isnull()]

# 將index改成年月日
df.index = pd.to_datetime((df['交易年月日'].str[:-4].astype(int) + 1911).astype(str) + df['交易年月日'].str[-4:] ,errors='coerce')

#df.to_csv('data.csv',encoding='utf-8-sig')

#每年房價走勢圖
prices = {}
for district in set(df['鄉鎮市區']):
    cond = (
        (df['主要用途'] == '住家用')
        & (df['鄉鎮市區'] == district)
        & (df['單價元坪'] < df["單價元坪"].quantile(0.95))
        & (df['單價元坪'] > df["單價元坪"].quantile(0.05))
        )
    
    groups = df[cond]['year']
    
    prices[district] = df[cond]['單價元坪'].astype(float).groupby(groups).mean().loc[2012:]
    
price_history = pd.DataFrame(prices)
price_history.plot()
plt.show()