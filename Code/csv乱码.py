import pandas as pd

csv_path = r'C:\Users\dawn_\Company_project\Data_File\public_data\6月数据.csv'
out_path = r'C:\Users\dawn_\Company_project\Data_File\public_data\6月直营销售商品汇总.xlsx'


def csv_to_excel(csv, excel):
    """将csv文件转换为excel文件
    csv,excel为输入与输出路径"""
    df = pd.read_csv(csv)
    print(df)
    df.to_excel(excel)
    print("工作结束")


csv_to_excel(csv_path, out_path)
