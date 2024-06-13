import pandas as pd
import mysql.connector

# 读取CSV文件
csv_file = 'assist.csv'
data = pd.read_csv(csv_file)

# 连接到MySQL数据库
db_connection = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='1234',
    database='ocean_surface_height',
    port=3306
)

cursor = db_connection.cursor()


# 创建插入SQL语句
insert_query1 = """
INSERT INTO `common_queryassist` (no_id, name, state)
VALUES (%s, %s, %s)
"""

# 创建插入SQL语句
insert_query2 = """
INSERT INTO `common_identityinfo` (no, password, belong)
VALUES (%s, %s, %s)
"""

# 遍历数据并插入到数据库中
for index, row in data.iterrows():
    cursor.execute(insert_query2, (row['id'], row['passwd'], "Q"))
    cursor.execute(
        insert_query1, (row['id'], row['name'], row['state']))


# 提交事务
db_connection.commit()

# 关闭连接
cursor.close()
db_connection.close()

print("Data inserted successfully.")
