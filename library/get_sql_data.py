import pandas as pd
from sqlalchemy import create_engine
from library.user import SqlServer

pd.set_option('display.unicode.east_asian_width', True)


class CallSQL:
    """
    根据数据库命令路径调取数据，生成DataFrame
    """

    def __init__(self, sql_path, database='my_data'):
        """
        :param sql_path: 文件路径
        """
        self.sql_path = sql_path
        self.sql = SqlServer
        self.database = database
        self.conn_parameter = f"mssql+pymssql://{self.sql.yaoud_user}:{self.sql.yaoud_password}@{self.sql.yaoud_IP}/{self.database}?charset=utf8"

    def read_sql_language(self):
        """
        读取SQL语句文本
        """
        with open(self.sql_path, 'r', encoding='utf-8') as open_file:
            sql_language = open_file.read()
        return sql_language

    def get_data(self):
        """
        根据语句获取data
        :return DataFrame
        """
        engine = create_engine(self.conn_parameter, echo=False)
        sql_language = self.read_sql_language()  # 获取sql语句
        with engine.connect() as conn:
            data = pd.read_sql(sql_language, con=conn)
        return data

    def implement(self):
        """
        根据SQL Server语句对数据库进行操作
        """
        engine = create_engine(self.conn_parameter, echo=False)
        sql_language = self.read_sql_language()
        with engine.connect() as con:
            con.execute(sql_language)
        print('Mission accomplished!')


if __name__ == '__main__':
    path = r'C:\Users\dawn_\Company_project\sql_command\text1.sql'
    df = CallSQL(path)
    print(df.get_data())
