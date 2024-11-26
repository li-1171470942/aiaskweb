import pandas as pd


# 读取csv文件，并将内容以二维列表的形式返回
def read_csv_to_list(file_path):
    df = pd.read_csv(file_path)
    return df.values.tolist()


# 将二维列表数据存为一个csv文件，并指定名称和存储路径
def save_list_to_csv(data, file_path):
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)


# 将panda表格对象存为一个csv文件，并指定名称和存储路径
def save_dataframe_to_csv(df, file_path):
    try:
        df.to_csv(file_path, index=False)
        print("save success, name is "+file_path)
    except:
        print("save fail")


# 创建一个空的panda表格对象并返回
def create_empty_dataframe(columns=None):
    return pd.DataFrame(columns=columns)


# 得到panda表格对象的内容（指定行）
def get_dataframe_row(df, row_index):
    return df.iloc[row_index]


# 得到panda表格对象的内容（指定列）
def get_dataframe_column(df, column_name):
    return df[column_name]


# 得到panda表格对象的内容（指定行、列）
def get_dataframe_cell(df, row_index, column_name):
    return df.at[row_index, column_name]


# 得到panda表格对象的行数（指定列）
def get_dataframe_row_count(df):
    return len(df)


# 得到panda表格对象的列数（指定行）
def get_dataframe_column_count(df):
    return len(df.columns)


# 给panda表格对象增加一行内容
def append_row_to_dataframe(df, row_data):
    # 将 row_data 转换为 DataFrame，如果 row_data 本身是字典或类似格式
    row_df = pd.DataFrame([row_data])

    # 使用 pd.concat 合并 DataFrame
    df = pd.concat([df, row_df], ignore_index=True)

    return df


# 给panda表格对象指定表头
def set_dataframe_headers(df, headers):
    df.columns = headers
    return df


# 给panda表格对象插入数据（指定行）
def insert_row_to_dataframe(df, row_index, row_data):
    df.loc[row_index] = row_data
    return df


# 给panda表格对象插入数据（指定列）
def insert_column_to_dataframe(df, column_name, column_data):
    df[column_name] = column_data
    return df


# 给panda表格对象插入数据（指定行、列）
def insert_cell_to_dataframe(df, row_index, column_name, value):
    df.at[row_index, column_name] = value
    return df
