from django.shortcuts import render
from django.http import JsonResponse
from api.main import *
from api.zhiliao import *
from django.http import FileResponse, Http404
import os

scraper = None

data = {
    "page_size": 0,
    "progress1": [0, 1],
    "progress2": [0, 1],
    "progress3": [0, 1],
    "progress4": [0, 1],
}


def download_file(request):
    # 文件路径逻辑 -- 例如，基于某种业务逻辑或数据库查询
    path = get_parent_directory() + '\\data\\resultCSV'
    file_path = list_txt_files_sorted_by_creation_time(path, 'csv')[-1]
    print(file_path)

    # 确保文件存在并发送给客户端
    if os.path.exists(file_path):
        filename = os.path.basename(file_path)
        response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)
        return response
    else:
        raise Http404("File not found")


# 由前端每两秒触发，获得data的数据，来实时更新前端的内容
def getData(request):
    global data
    return JsonResponse(data)


# 前端触发，来改变page_size的值
def update_page_size(request):
    global scraper
    if scraper is None:
        scraper = WebScraper()
    global data
    try:
        # 假设 scraper.getPageSize() 是可以调用的方法
        data['page_size'] = scraper.getPageSize()
        data['progress1'][1] = data['page_size']
        print(data['page_size'])
        res = {
            'code': 0,
            'data': data
        }
        return JsonResponse(res)
    except Exception as e:  # 更具体的异常处理
        print(f'Error occurred: {e}')
        res = {
            'code': -1,
            'data': None
        }
        return JsonResponse(res)


# 前端触发，获得所有的文章的url
def getUrls(request):
    global scraper
    if scraper is None:
        scraper = WebScraper()
    global data
    try:
        base_url = 'https://zhiliao.h3c.com'
        sub_url = '/theme/index/6_1______all?themeSearchKey=&search_type=1&p='
        sub_urlList = []
        list1 = [x for x in range(0, int(data['page_size']))]
        for i in list1:
            print('page ', i, ' of total ', len(list1))
            data['progress1'][0] = i + 1
            try:
                res = scraper.webmock(base_url + sub_url + str(i),
                                      scraper.getSubUrl)
                time.sleep(4)
                sub_urlList.extend(res)
            except:
                print("[getSub_urlList] webmock error ,i =", i)
                pass

        sub_urlList = list(set(sub_urlList))
        sub_urlList = [base_url + x for x in sub_urlList]
        print(sub_urlList)

        path = get_parent_directory() + '/data/urlList/'
        create_directory_in_root(path)
        save_result_to_file(sub_urlList, path + getNowTimeStr() + 'urlList.txt')

    except Exception as e:  # 更具体的异常处理
        print(f'Error occurred: {e}')
        res = {
            'code': -1,
            'data': None
        }
        return JsonResponse(res)

    res = {
        'code': 0,
        'data': data
    }
    return JsonResponse(res)


# 前端触发，或者所有文章的原始文本资料
def getOriginText(request):
    global scraper
    if scraper is None:
        scraper = WebScraper()
    global data
    try:
        path = os.path.join(get_parent_directory(), 'data', 'urlList')
        create_directory_in_root(path)
        fileName = list_txt_files_sorted_by_creation_time(path, 'urlList.txt')
        urlList = []
        for name in fileName:
            urlList.extend(load_result_from_file(name))

        urlList = list(set(urlList))
        print(urlList)
        result = []
        data['progress2'][1] = len(urlList)
        for i, url in enumerate(urlList):
            print(i + 1, ' of total ', len(urlList))
            data['progress2'][0] = i + 1
            try:
                s = scraper.webmock(url, scraper.grepText)
                s = remove_whitespace_and_newlines(s)
                time.sleep(5)
                if s == "":
                    continue
                result.append([s, url])
            except:
                continue

        path = get_parent_directory() + '/data/Odata/'
        create_directory_in_root(path)
        save_result_to_file(result, path + getNowTimeStr() + 'Odata.txt')

    except Exception as e:  # 更具体的异常处理
        print(f'Error occurred: {e}')
        res = {
            'code': -1,
            'data': None
        }
        return JsonResponse(res)

    res = {
        'code': 0,
        'data': data
    }
    return JsonResponse(res)


def askAI(request):
    global data
    try:
        path = get_parent_directory() + '\\data\\Odata'
        ss = getFileFromList2list(path, 'Odata.txt')

        temp = set()

        path = get_parent_directory() + '\\data\\TYresult'
        res = getFileFromList2list(path, 'TYresult.txt')  # 已经得到ai回答的结果
        for o in res:
            url = o["原始网站"]
            temp.add(url)

        wait2ask = []

        # 避免重复提问，确保一个url只问一次
        for s, url in ss:
            if url in temp:
                continue
            else:
                wait2ask.append([s, url])
                temp.add(url)

        if len(wait2ask) == 0:
            print("没有需要问AI的")
            raise NegativeNumberError("no need to ask AI")

        account = "ai_wxlx"
        password = "Aiwxlx12!"
        token = get_token(account, password)
        if token:
            print(f"获取到的token: {token}")
        else:
            print("未能获取token")
            raise NegativeNumberError("Cannot get token")

        data['progress3'][1] = len(wait2ask)
        cnt = 0
        result = []
        witeTime = 10
        path = get_parent_directory() + '\\data\\TYresult\\'
        print(len(wait2ask))
        data['progress3'][1] = len(wait2ask)
        for s, url in wait2ask:
            startTime = time.time()
            getDataStr = '帮我将上述内容总结，用问题现象、问题描述、结论、解决办法等四个方面描述'
            response = askTongyiqianwen(s + getDataStr, token)
            print('response: ',response)
            if response == "":
                print('ask error or overTime', url)
                token = get_token(account, password)
                if token:
                    print(f"获取到的token: {token}")
                    response = askTongyiqianwen(s + getDataStr, token)
                else:
                    print("未能获取token")
                    raise NegativeNumberError("Cannot get token")
            text = markdown_to_text(response)
            text = remove_whitespace_and_newlines(text)

            res = {}  # 解析ai的答案
            temp = extract_problem_details(text)
            if temp == {}:
                print('get no valid res', url)
                continue
            res.update(temp)  # 解析ai的答案
            result.append(res)  # 添加到结果中
            res['原始网站'] = url
            res['备注'] = ''
            print(res)

            useTime = calculate_time_difference(startTime, time.time())
            cnt += 1
            data['progress3'][0] = cnt
            print(str(cnt) + ' out of total ' + str(len(ss)), 'useTime:', useTime)
            # 限制接口请求频率
            if useTime < witeTime:
                time.sleep(witeTime - useTime + 1)
            if cnt % 20 == 0:
                create_directory_in_root(path)
                save_result_to_file(result, path + getNowTimeStr() + 'TYresult.txt')
                result.clear()

        save_result_to_file(result, path + getNowTimeStr() + 'TYresult.txt')

    except NegativeNumberError as e:
        print(f"An error occurred: {e}")
        res = {
            'code': -1,
            'data': None
        }
        return JsonResponse(res)
    except Exception as e:  # 更具体的异常处理
        print(f'Error occurred: {e}')
        res = {
            'code': -2,
            'data': None
        }
        return JsonResponse(res)
    res = {
        'code': 0,
        'data': None
    }
    return JsonResponse(res)


def outPutResult(request):
    global data
    try:
        temp = set()
        path = get_parent_directory() + '\\data\\TYresult'
        res = getFileFromList2list(path, 'TYresult.txt')  # 已经得到ai回答的结果
        cnt = 0
        df = create_empty_dataframe()
        for o in res:
            if o['原始网站'] in temp:
                continue
            else:
                temp.add(o['原始网站'])
                res = {'序号': cnt, '问题现象': o['问题现象'], '问题描述': o['问题描述'], '结论': o['结论'],
                       '解决办法': o['解决办法'], '原始网站': o['原始网站'], '备注': o['备注']}
                df = append_row_to_dataframe(df, res)
                cnt += 1
        if cnt != 0:
            path = get_parent_directory() + '\\data\\resultCSV\\'
            create_directory_in_root(path)
            save_dataframe_to_csv(df, path + getNowTimeStr() + '.csv')

    except Exception as e:  # 更具体的异常处理
        print(f'Error occurred: {e}')
        res = {
            'code': -1,
            'data': None
        }
        return JsonResponse(res)

    res = {
        'code': 0,
        'data': None
    }
    return JsonResponse(res)


def home(request):
    # Example progress values

    return render(request, 'staticpage/home.html', {
    })


if __name__ == '__main__':
    path = get_parent_directory() + '\\data\\resultCSV\\'
    create_directory_in_root(path)
