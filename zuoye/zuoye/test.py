import csv


import pandas as pd
from django.shortcuts import render


def home_view():
    # 指定CSV文件路径，这里假设caipu.csv位于项目根目录
    csv_file_path = './caipu.csv'
    if csv_file_path:
        csv_data = pd.read_csv(csv_file_path)
        print(csv_data)
    else:
        print('无数据链接')
    csv_data_lsit = csv_data.to_dict('records')

    print(csv_data_lsit)
if __name__ == '__main__':
    home_view()







