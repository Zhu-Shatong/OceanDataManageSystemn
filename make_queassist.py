import pandas as pd
import random
from faker import Faker
import csv

# 初始化 Faker 库
fake = Faker('zh_CN')

# 初始化数据列表
data = []


# 生成数据
for i in range(50):
    record_id = 2001 + i
    passwd = 'q123456'
    belong = 'Q'
    name = fake.name()
    state = 0
    data.append([record_id, passwd, belong, name, state])

# 创建 DataFrame
df = pd.DataFrame(
    data, columns=['id', 'passwd', 'Belong', 'name', 'state'])

# 保存为 CSV 文件
df.to_csv('assist.csv', index=False,
          quoting=csv.QUOTE_NONNUMERIC, encoding='utf-8-sig')

print("CSV 文件已生成。")
