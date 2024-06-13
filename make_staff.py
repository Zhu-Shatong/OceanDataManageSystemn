import csv
import random
from faker import Faker
import pandas as pd

# Initialize Faker
fake = Faker('zh_CN')

# Constants
depart_name = [
    "气候变化研究（全球变暖、冰川和冰盖）", "海洋学研究（海洋动力学和潮汐）",
    "地质学研究（海岸线变化和沉积）", "课堂教学", "沿海开发和建设", "保险业",
    "海运和港口管理", "开发商业应用程序", "户外活动和旅游", "个人决策制定",
    "个人数据分析项目", "天气预报", "气候模型", "洋流", "海啸预警",
    "风暴潮预警", "沿海洪水风险管理", "厄尔尼诺"
]

profession = ["负责人", "行业专家", "研究员", "研究员", "审核专员", "审核专员"]

# Helper functions


def generate_time(begin, end):
    return f'{random.randint(begin, end)}:00'


# Generate CSV data
rows = []
id_counter = 1000001

for depart in depart_name:
    for i in range(6):
        row = {
            "id": id_counter,
            "passwd": "s123456",
            "Belong": "S",
            "name": fake.name(),
            "depart": depart,
            "profession": profession[i],
            "score": 10.00,
            "time-begin": generate_time(6, 8),
            "time-end": generate_time(16, 23)
        }
        rows.append(row)
        id_counter += 1

# Convert list of dictionaries to DataFrame
df = pd.DataFrame(rows)

# Save DataFrame to CSV
output_csv = 'staff.csv'
df.to_csv(output_csv, index=False, encoding='utf-8')
print(f"CSV file generated: {output_csv}")
