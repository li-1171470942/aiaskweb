import json
from datetime import datetime
import os
import sys
from selenium.webdriver.chrome.options import Options
import socket
import re


def getFileFromList2list(path, tail='.txt'):
    create_directory_in_root(path)
    fileName = list_txt_files_sorted_by_creation_time(path, tail)
    ss = []
    for name in fileName:
        ss.extend(load_result_from_file(name))
    return ss


class NegativeNumberError(Exception):
    pass


# markdown转txt
def markdown_to_text(markdown_text):
    # 去掉标题 ('# ', '## ', '### ', 等)
    text = re.sub(r'#+ ', '', markdown_text)

    # 去掉粗体和斜体标记 ('**', '__', '*', '_')
    text = re.sub(r'(\*\*|__|\*|_)(.*?)\1', r'\2', text)

    # 去掉横线 (---)
    text = re.sub(r'---+|\*\*\*+', '', text)

    # 去掉列表前的符号 ('-', '*', '+')
    text = re.sub(r'^[-*+] ', '', text, flags=re.MULTILINE)

    # 清理多余的连续换行符
    text = re.sub(r'\n+', '\n', text).strip()

    return text


# 比较两个时间，单位是秒
def calculate_time_difference(time1, time2):
    """
    计算两个时间戳之间的差异，单位是秒。

    :param time1: 第一个时间戳（从time.time()获取）
    :param time2: 第二个时间戳（从time.time()获取）
    :return: 两个时间戳之间的差值（秒）
    """
    # 计算差异
    difference = abs(time1 - time2)
    return difference


# 获得当前ip
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # 这行代码不会实际发送数据到8.8.8.8，只会用于得到合适的出口接口
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
    except Exception:
        ip_address = '127.0.0.1'
    finally:
        s.close()
    return ip_address


# 自定义文本解析器
def extract_problem_details(text):
    # 定义要查找的部分关键字
    sections = ["问题现象", "问题描述", "结论", "解决办法"]
    # 用于存储每个部分起始索引的字典
    extracted_details = {}

    # 找到每个部分的起始位置
    for section in sections:
        start_index = text.find(section)
        if start_index != -1:
            extracted_details[section] = start_index

    # 如果未找到任何部分，则返回错误信息
    if not extracted_details:
        print("未找到任何匹配的部分 ", text)
        return {}  # 返回一个空字典而不是 None

    # 按起始位置对部分进行排序
    sorted_sections = sorted(extracted_details.items(), key=lambda x: x[1])

    # 初始化结果字典
    results = {section: '' for section in sections}

    # 提取各个部分的内容
    for i in range(len(sorted_sections) - 1):
        # 提取当前部分的内容，直到下一个部分开始
        start_text = sorted_sections[i][0]
        end_index = sorted_sections[i + 1][1]
        content = text[sorted_sections[i][1] + len(start_text):end_index].strip()
        results[start_text] = content

    # 提取最后一个部分的内容
    last_start_text = sorted_sections[-1][0]
    last_content = text[sorted_sections[-1][1] + len(last_start_text):].strip()
    results[last_start_text] = last_content

    return results


# 返回特定路径下，特定后缀的文件列表，以创建时间为排序
def list_txt_files_sorted_by_creation_time(path, tail='.txt'):
    """
    列出当前目录中所有以.txt为后缀的文件，并按照创建时间排序返回。
    """
    if path is None:
        path = os.path.dirname(os.path.abspath(__file__))

    # 列出目录中所有以.txt为后缀的文件
    txt_files = [
        f for f in os.listdir(path)
        if os.path.isfile(os.path.join(path, f)) and f.endswith(tail)
    ]
    txt_files = [path + '\\' + f for f in txt_files]
    # 按创建时间排序文件列表
    txt_files.sort(key=lambda f: os.path.getctime(os.path.join(path, f)))

    return txt_files


# 删除字符串的空格和换行符
def remove_whitespace_and_newlines(input_string):
    """
    去除字符串中的所有换行符和空格。

    :param input_string: 原始字符串
    :return: 去除换行符和空格后的字符串
    """
    # 去除所有的换行符和空格
    stripped_string = ''.join(input_string.split())
    return stripped_string


def getRootDirectory():
    return os.path.dirname(os.path.abspath(__file__))


def get_parent_directory():
    # 获取当前程序的绝对目录
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # 获取上一级目录
    parent_directory = os.path.dirname(current_directory)

    return parent_directory


def create_directory_in_root(directory_name):
    # 获取当前程序根目录
    root_directory = getRootDirectory()

    # 构造新目录的完整路径
    new_directory_path = os.path.join(root_directory, directory_name)
    print(new_directory_path)

    # 检查目录是否已经存在
    if not os.path.exists(new_directory_path):
        try:
            os.makedirs(new_directory_path)
            print(f"Directory '{directory_name}' created successfully in root directory.")
        except Exception as e:
            print(f"Failed to create directory '{directory_name}': {e}")
    else:
        print(f"Directory '{directory_name}' already exists in root directory.")


# 将对象存为文件
def save_result_to_file(result, filename='data.txt'):
    """
    将结果列表保存到文件。
    :param result: 需要保存的结果列表
    :param filename: 保存的文件名
    """
    try:
        # 将数据序列化并写入文件
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(result, file, ensure_ascii=False, indent=4)
        print(f"Data successfully saved to {filename}.")
    except Exception as e:
        print(f"Failed to save data: {e}")


# 将文件数据转为对象
def load_result_from_file(filename='data.txt'):
    """
    从文件中读取结果列表。
    :param filename: 要读取的文件名
    :return: 读取到的结果列表
    """
    try:
        # 读取文件并反序列化数据
        with open(filename, 'r', encoding='utf-8') as file:
            result = json.load(file)
        print(f"Data successfully loaded from {filename}.")
        return result
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []
    except json.JSONDecodeError:
        print(f"Failed to decode JSON from {filename}.")
        return []
    except Exception as e:
        print(f"Failed to load data: {e}", filename)
        return []


# 获得当前时间的字符串
def getNowTimeStr(Format="%Y-%m-%d_%H-%M-%S"):
    current_time = datetime.now()
    file_name = current_time.strftime(Format)
    return file_name


def split_list(original_list, max_length):
    """
    将一个列表按照指定的最大长度分为多个子列表。

    :param original_list: 要拆分的原始列表。
    :param max_length: 每个子列表的最大长度。
    :return: 拆分后的子列表集合。
    """
    return [original_list[i:i + max_length] for i in range(0, len(original_list), max_length)]


def split_list_into_parts(original_list, num_parts):
    """
    将一个列表分为指定数量的子列表。

    :param original_list: 要拆分的原始列表。
    :param num_parts: 需要拆分成的子列表数量。
    :return: 拆分后的子列表集合。
    """
    if num_parts <= 0:
        raise ValueError("num_parts must be greater than 0")

    # 计算每个子列表的基础长度，以及需要多一个元素的子列表数量
    total_length = len(original_list)
    base_length = total_length // num_parts
    longer_parts = total_length % num_parts

    sublists = []
    start = 0
    for i in range(num_parts):
        # 确定当前子列表的结束索引
        end = start + base_length + (1 if i < longer_parts else 0)
        sublists.append(original_list[start:end])
        start = end

    return sublists


# 示例使用
if __name__ == '__main__':
    create_directory_in_root('newdir')
