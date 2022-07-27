import os

import pandas as pd

pd.set_option('display.unicode.east_asian_width', True)


def df_split(input_path, split_num, out_path, out_name='拆分表', table_name='Sheet1'):
    """
    根据导入的csv，生成指定数量的表格，并保存到指定目录下
    :param input_path: 数据表格所在路径。
    :param split_num: 拆分数量，因为除不尽的原因，所输出的表会比此数字大1。
    :param out_path: 所要保存的文件目录路径。
    :parameter out_name: 索要保存的文件名称。默认为(拆分表)
    :parameter table_name: excel中子表名称，默认为(Sheet1)
    :return:
    """
    df = pd.read_csv(input_path)
    rows = len(df.iloc[:, 0]) // split_num  # 每一组数据的行数
    b = 0  # 文件计数
    a = 0  # 确定行位置
    while a < len(df.iloc[:, 0]):
        data = df.iloc[a:(a + rows)]
        b += 1
        # 将获取到的路径转换为绝对路径（os.path.abspath），并与目录名称组合成文件路径(os.path.join)
        data.to_excel(os.path.join(os.path.abspath(out_path), f'{out_name}{b}.xls'))
        a = a + rows
    print(f"已完成任务，共拆分{b}张表.")


path = r"C:\Users\dawn_\Desktop\临时数据\tsyykc.csv"  # 需要拆分的表的绝对路径
path_out = r"C:\Users\dawn_\Desktop\临时数据"  # 拆分后生成的表的存放文件夹的绝对路径
name = "库存"  # 拆分后生成的表的文件名
number = 2  # 需要拆分的份数，因为存在不能整除的因素，一般生成的表会比这个数字大1
df_split(path, number, path_out, name)
