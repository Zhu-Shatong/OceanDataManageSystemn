import mysql.connector
from my_rsa import *

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
insert_query = """
INSERT INTO `common_dataset` (d_name, d_presc)
VALUES (%s, %s)
"""

d_name_template = "{}年海洋表面高度数据"
url_template = "http://localhost:8501/?encrypted_message={}"

# 先清空表
cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
cursor.execute("TRUNCATE TABLE `common_dataset`")
cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

# 从2017年到1992年
for i in range(2017, 1991, -1):
    d_name = d_name_template.format(i)
    d_presc = url_template.format(encrypt_message(str(i)))
    cursor.execute(insert_query, (d_name, d_presc))

# 提交事务
db_connection.commit()

# 关闭连接
cursor.close()
db_connection.close()

print("Data inserted successfully.")
