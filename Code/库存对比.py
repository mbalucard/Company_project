import pandas as pd
from sqlalchemy import create_engine
from library.user import SqlServer
from library import json_data as jd
from library.user import CloudWarehouse
from library.get_sql_data import CallSQL

pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.max_columns', 5)  # 设置最大列数


def name_and_date(table_name, database='my_data'):
    """
    判断表是否存在且创建时间是否是当天
    :param table_name: 表名
    :param database: 数据库名称
    :return:
    """
    sql_language = """select name,
       convert(varchar(100),create_date,23) as date,
       convert(varchar(100),getdate(),23) as today
        from sys.tables"""
    sql = SqlServer
    engine = create_engine(
        f"mssql+pymssql://{sql.yaoud_user}:{sql.yaoud_password}@{sql.yaoud_IP}/{database}?charset=utf8", echo=False)
    with engine.connect() as conn:
        data = pd.read_sql(sql_language, con=conn)
    names = list(data['name'])
    if table_name in names:
        df = data.loc[data['name'] == table_name]
        if list(df['date']) == list(df['today']):
            return True
        else:
            return False
    else:
        return False


def get_stock():
    """
    获取云仓库存
    :return:
    """
    cloud = CloudWarehouse
    data = {
        "Goods_No": "",
        "Lot_No": "",
        "Stock_Status": "",
        "Operator_Id": cloud.Operator_Id,
        "Con_Id": cloud.Con_Id,
        "Ldc_Id": cloud.Ldc_Id
    }
    category = "kc"
    df = jd.cloud_warehouse(data, category)
    print(df.info())
    jd.to_sql(df, tb_name, exists='replace')


sql_path = r'/Data_File/sql_data/库存对比.sql'
tb_name = 'yc_kc'
referee = name_and_date(tb_name)
difference = CallSQL(sql_path, database='yaoud')

if referee:
    print('库存对比中，请稍后...')
    df = difference.get_data()
else:
    print('正在刷新库存,请耐心等待...')
    get_stock()
    print('库存对比中,请稍后...')
    df = difference.get_data()

print(df.info())
df.to_excel(r'C:\Users\dawn_\Company_project\Data_File\public_data\7-26差异.xlsx')
