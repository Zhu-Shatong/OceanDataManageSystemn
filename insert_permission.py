import pandas as pd
import mysql.connector

# 读取CSV文件
csv_file = 'permission.csv'
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

# 获取当前最大的 p_index 值
cursor.execute(
    "SELECT MAX(p_index) FROM `common_permission`")
max_p_index = cursor.fetchone()[0]
if max_p_index is None:
    max_p_index = 0

# 创建插入SQL语句
insert_query = """
INSERT INTO `common_permission` (p_index, p_no, p_depict)
VALUES (%s, %s, %s)
"""

# 清空数据库
cursor.execute("TRUNCATE TABLE `common_permission`")

# 遍历数据并插入到数据库中
for index, row in data.iterrows():
    max_p_index += 1
    cursor.execute(insert_query, (max_p_index, row['no'], row['depict']))

# 提交事务
db_connection.commit()

# 关闭连接
cursor.close()
db_connection.close()

print("Data inserted successfully.")
