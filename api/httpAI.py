import time

import requests
import json

from api.utils import *


# 得到token
def get_token(account, password):
    url = "https://api-ai.h3c.com/session/api/user/login"
    headers = {
        'Auth-Type': 'DB',
        'Content-Type': 'application/json'
    }
    payload = {
        "account": account,
        "password": password
    }

    try:
        # 发送POST请求
        response = requests.post(url, json=payload, headers=headers)

        # 检查响应状态码
        response.raise_for_status()

        # 解析JSON响应
        json_response = response.json()
        # 检查code是否为0，表示成功
        if json_response.get("code") == 0:
            # 返回token
            return json_response.get("token")
        else:
            print(f"请求失败: {json_response.get('msg')}")
            return None

    except requests.RequestException as e:
        print(f"HTTP请求出现错误: {e}")
        return None


# 问ai 通义千问 api
def call_lin_seer_api(token, chat_content, role, ip, user_id, session_id=None, create_session=True,
                      multiple_chat=False):
    url = "https://api-ai.h3c.com/session/ai/chat/linSeer"
    headers = {
        "Content-Type": "application/json",
        "Authorization": token
    }

    # 构造请求体
    data = {
        "chatInfo": {
            "content": chat_content,
            "role": role
        },
        "stream": False,
        "createSession": create_session,
        "ip": ip,
        "multipleChat": multiple_chat,
        "requestSource": "PC",
        "model": "QIANWEN",
        "userId": user_id
    }

    # 可选sessionId参数
    if multiple_chat and session_id is not None:
        data["sessionId"] = session_id

    # 发送POST请求
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # 处理返回结果
    if response.status_code == 200:
        try:
            return response.json()
        except json.JSONDecodeError:
            return {"error": "Invalid JSON response"}  # 如果返回的不是JSON，处理错误
    else:
        return {"error": f"Request failed with status {response.status_code}"}


# 输入token和提问文本，问ai
def askTongyiqianwen(askMessage, token):
    if len(askMessage) < 10:
        print('too short input str')
        return ""
    # 示例调用
    chat_content = askMessage
    role = "user"
    ip = get_ip_address()
    user_id = "l32524"

    response = call_lin_seer_api(token, chat_content, role, ip, user_id)
    try:
        # 提取content
        content_value = response.get('data', {}).get('message', {}).get('content')
        return content_value
    except:
        try:
            error_msg_str = response['data']['errorMsg']
            error_msg_dict = json.loads(error_msg_str)
            error_str = error_msg_dict['hitWord']

            stripped_string = error_str.replace("[", "")
            stripped_string = stripped_string.replace("]", "")
            stripped_string = stripped_string.replace("命中敏感词:", "")
            print("敏感词汇", stripped_string)

            newMessage = askMessage.replace(stripped_string, "")
            print("剔除再试一试", newMessage)
            time.sleep(5)
            return askTongyiqianwen(newMessage, token)
        except:
            print(response)
            return ""
