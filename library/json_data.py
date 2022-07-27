import requests
import pandas as pd
from sqlalchemy import create_engine
from library import user

pd.set_option('display.unicode.east_asian_width', True)  # 对齐
pd.set_option('display.max_columns', 5)  # 设置最大列数


def cloud_warehouse(js_code, category, star=4):
    """
    根据json语句查询云仓信息
    :param js_code: 查询语句
    :param category: 执行的操作类别
    :parameter star: 输出DataFrame 从第几列开始，默认第4列
    :return: DataFrame
    """
    cloud = user.CloudWarehouse
    url = cloud.url  # 接口网址
    json_data = {
        "funcType": "select",  # 方法类别
        "callCategory": category,  # 操作类别
        "id": cloud.id,
        "pwd": cloud.password,
        # 字段内容
        "jsondata": js_code}

    res = requests.post(url=url, json=json_data)  # 用Post方法调用接口
    js_data = res.json()  # 解析获取到的数据，这里是json,解析后的数据类型为dict

    if js_data['Flag'] is False:
        print("警告:", js_data['ErrInfo'])
    else:
        if js_data["MsgInfo"]:
            js_msg_info = js_data["MsgInfo"]  # 截取dict中自己要的值
            # key = list(js_MsgInfo[0].keys())  # 获取dict中的key值，并放在list中
            basket = list()  # 一篮子计划，你懂的
            for dict_i in js_msg_info:
                # 用dict生成dataframe,必须指定index,这里的index为dict中的key值
                df_i = pd.DataFrame.from_dict(dict_i, orient='index')
                basket.append(df_i.T)  # 因为index 为key值，所以要做矩阵转置
            df = pd.concat(basket, ignore_index=True)  # 按列明组合，并重新定义index
            df = df.iloc[:, star:]  # 去掉前面无用数值
            return df
        else:
            return js_data


def to_sql(data_frame, table_name, database='my_data', exists='fail'):
    """
    将DataFrame插入至数据库
    :param data_frame: DataFrame格式数据
    :param table_name: 表名称
    :parameter database: 数据库名称，默认为:my_data
    :parameter exists: 如果表名称存在则报错，可改为：replace替换、append追加
    :return:
    """
    sql = user.SqlServer
    engine = create_engine(
        f"mssql+pymssql://{sql.yaoud_user}:{sql.yaoud_password}@{sql.yaoud_IP}/{database}?charset=utf8", echo=False)
    data_frame.to_sql(table_name, engine, index=False, if_exists=exists)  # 有replace替换、append追加
    print(f'{table_name} 表已添加至 {database}')


if __name__ == '__main__':
    all_id = user.CloudWarehouse
    data = {
        "Operator_Id": all_id.Operator_Id,
        "Con_Id": all_id.Con_Id,
        "Ldc_Id": all_id.Ldc_Id,
        "Businessbill_No": "",
        "Goods_No": "",
        "Start_Date": "2022-07-07",
        "End_Date": "2022-07-07"
    }

    operation = "kcztbh"

    js = cloud_warehouse(data, operation)
    print(js)
