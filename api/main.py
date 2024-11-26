from api.browserMock import *
import threading
from api.CSVapi import *
from api.httpAI import *


def run_in_threads(num_threads, callback, args_list=None, kwargs_list=None):
    """
    根据给定的整数数目创建线程数，并执行传入的回调函数。

    :param num_threads: 需要创建的线程数。
    :param callback: 每个线程所要执行的回调函数。
    :param args_list: 每个线程的参数列表。每个元素是传递给 callback 的位置参数元组。
    :param kwargs_list: 每个线程的关键词参数字典列表。每个元素是传递给 callback 的关键字参数字典。
    """
    if args_list is None:
        args_list = [()] * num_threads  # 默认情况下，每个线程不带位置参数

    if kwargs_list is None:
        kwargs_list = [{}] * num_threads  # 默认情况下，每个线程不带关键字参数

    # 创建并启动线程
    for i in range(num_threads):
        thread = threading.Thread(target=callback, args=(args_list[i][0], args_list[i][1]))
        thread.start()
        print(f"Thread-{i + 1} started with args: {args_list[i]}, kwargs: {kwargs_list[i]}")
        time.sleep(15)

    # 等待所有线程完成
    # for index, thread in enumerate(threads):
    #     thread.join()
    #     print(f"Thread-{index + 1} finished.")


# 通译千问问答应用
def dodododo():
    fileName = list_txt_files_sorted_by_creation_time(None, 'Odata.txt')[-1]
    ss = load_result_from_file(fileName)
    cnt = 0
    failText = []
    result = []
    witeTime = 10

    account = "ai_wxlx"
    password = "Aiwxlx12!"
    token = get_token(account, password)
    if token:
        print(f"获取到的token: {token}")
    else:
        print("未能获取token")
        return

    errorCnt = 0
    for s, url in ss:
        startTime = time.time()
        getDataStr = '帮我将上述内容总结，用问题现象、问题描述、结论、解决办法等四个方面描述'
        response = askTongyiqianwen(s + getDataStr, token)
        if response == "":
            print('ask error or overTime')
            failText.append([s, text, url])
            errorCnt += 1
            if errorCnt > 5:
                token = get_token(account, password)
                if token:
                    print(f"获取到的token: {token}")
                else:
                    print("未能获取token")
                    break
            continue
        errorCnt = 0
        text = markdown_to_text(response)
        text = remove_whitespace_and_newlines(text)

        data = {'序号': cnt}  # 解析ai的答案
        temp = extract_problem_details(text)
        if temp == {}:
            print('get no valid data', url)
            failText.append([s, text, url])
            continue
        data.update(temp)  # 解析ai的答案
        result.append(data)  # 添加到结果中
        data['原始网站'] = url
        data['备注'] = ''
        print(data)
        useTime = calculate_time_difference(startTime, time.time())
        print(str(cnt) + ' out of total ' + str(len(ss)), 'useTime:', useTime)
        # 限制接口请求频率
        if useTime < witeTime:
            time.sleep(witeTime - useTime + 1)
        cnt += 1

        if cnt % 20 == 0:
            save_result_to_file(result, getNowTimeStr() + 'TYresult.txt')
            result.clear()

    save_result_to_file(result, getNowTimeStr() + 'TYresult.txt')
    save_result_to_file(failText, getNowTimeStr() + 'TYfailText.txt')
    result.clear()

    path = 'D:\\lxx9527\\project\\webCrawlerPY\\'
    filelist = list_txt_files_sorted_by_creation_time(path, 'TYresult.txt')
    result = []

    for name in filelist:
        obj = load_result_from_file(path + name)
        result.extend(obj)

    df = create_empty_dataframe()
    for i, o in enumerate(result):
        df = append_row_to_dataframe(df, o)

    save_dataframe_to_csv(df, getNowTimeStr() + 'TYresult.csv')


def makeCSV():
    path = 'D:\\lxx9527\\project\\webCrawlerPY\\'
    filelist = list_txt_files_sorted_by_creation_time(path, 'AIresult.txt')
    result = []

    for name in filelist:
        obj = load_result_from_file(path + name)
        result.extend(obj)

    # 将字典转换为 JSON 字符串来进行集合操作
    result_set = set(json.dumps(d, sort_keys=True) for d in result)

    # 可选：重新转换回字典
    unique_result = [json.loads(item) for item in result_set]
    print(unique_result)

    df = create_empty_dataframe()
    for i, o in enumerate(unique_result):
        data = {}
        data['序号'] = i
        stack = []
        # 遍历字典的所有键值对
        for key, value in reversed(list(o.items())):
            if isinstance(value, str) and value and (value[0] == ':' or value[0] == '：'):  # 检查字符串是否为空
                # 如果字符串的第一个是冒号或中文冒号，则去除，并改变原字典中的数据
                o[key] = value[1:]
                data[key] = o[key]  # 更新修正的值到data
            else:
                data[key] = value
        df = append_row_to_dataframe(df, data)

    save_dataframe_to_csv(df, getNowTimeStr() + '.csv')


def makeFailTextGreatAgain():
    path = 'D:\\lxx9527\\project\\webCrawlerPY\\'
    filelist = list_txt_files_sorted_by_creation_time(path, 'failText.txt')
    result = []

    for name in filelist:
        obj = load_result_from_file(path + name)
        result.extend(obj)

    # 将字典转换为 JSON 字符串来进行集合操作
    result_set = set(json.dumps(d, sort_keys=True) for d in result)

    # 可选：重新转换回字典
    unique_result = [json.loads(item) for item in result_set]
    print(unique_result)

    # 将之前失败的再次尝试一下
    todoAsk(unique_result, None)


if __name__ == '__main__':
    # run_in_threads(2, done, [[0, 800], [800, 1600]])
    # makeCSV()
    # time.sleep(60*60*5)

    dodododo()
