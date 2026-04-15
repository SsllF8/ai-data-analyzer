"""生成示例销售数据"""
import pandas as pd
import numpy as np
import random

np.random.seed(42)
random.seed(42)

regions = ['华北', '华东', '华南', '西南', '西北']
products = ['智能手表Pro', '无线耳机X1', '便携音箱M3', '充电宝S2', '蓝牙键盘K1']
channels = ['线上直营', '天猫旗舰店', '京东自营', '线下门店', '分销商']
salespeople = ['张伟', '李娜', '王磊', '赵敏', '陈浩', '刘芳', '杨涛', '黄丽', '周强', '吴燕']

prices = {
    '智能手表Pro': 1299,
    '无线耳机X1': 399,
    '便携音箱M3': 259,
    '充电宝S2': 149,
    '蓝牙键盘K1': 189,
}

rows = []
for month in range(1, 13):
    for _ in range(random.randint(25, 45)):
        date = f'2025-{month:02d}-{random.randint(1,28):02d}'
        product = random.choice(products)
        region = random.choice(regions)
        channel = random.choice(channels)
        person = random.choice(salespeople)
        qty = random.randint(1, 20)
        unit_price = prices[product]
        # 季节性趋势（Q4销量高）和区域差异
        seasonal = 1.0 + (month - 6) * 0.03 + (1 if month >= 10 else 0) * 0.2
        region_factor = {'华北': 1.1, '华东': 1.3, '华南': 1.2, '西南': 0.8, '西北': 0.6}[region]
        actual_qty = max(1, int(qty * seasonal * region_factor))
        amount = actual_qty * unit_price
        cost = int(amount * random.uniform(0.55, 0.68))
        rows.append([date, product, region, channel, person, actual_qty, unit_price, amount, cost, amount - cost])

df = pd.DataFrame(rows, columns=['日期', '产品', '区域', '渠道', '销售员', '数量', '单价', '销售额', '成本', '利润'])
output_path = r'c:\Users\liuzh\WorkBuddy\20260415161425\ai-data-analyzer\sample_data\2025年销售数据.xlsx'
df.to_excel(output_path, index=False)
print(f'Generated {len(df)} rows')
print(df.head(3).to_string())
print(f'Columns: {list(df.columns)}')
col = '销售额'
print(f'Total sales: {df[col].sum():,.0f}')
