from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import base64


async def start_http_server(port):
    print("1")
    server_address = ('0.0.0.0', port)
    print("2")
    httpd = HTTPServer(server_address, MyHTTPRequestHandler)
    print("3")
    print(f'Starting HTTP server on port {port}...')
    httpd.serve_forever()


# 创建一个自定义的请求处理类
class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # parsed_path = urlparse(self.path)
        # query_parameters = parse_qs(parsed_path.query)
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        # self.wfile.write("Received parameters: {}".format(query_parameters).encode('utf-8'))
        self.wfile.write("ok".encode('utf-8'))
        self.req_parameters = base64.b64decode(self.path[1:])
        # print(self.path[1:])
        print(self.req_parameters.decode('utf-8'), end='')
        # print()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        post_params = parse_qs(post_data)

        # 处理获取到的 POST 参数
        if 'echo' in post_params:
            param_value = post_params['echo'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            # self.wfile.write(f'You sent the following parameter: {param_value}'.encode('utf-8'))
            print(param_value)
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write('Parameter not found'.encode('utf-8'))

    def log_request(self, code='-', size='-'):
        pass

#
# # 设置服务器地址和端口
# server_address = ('0.0.0.0', 8181)  # 使用空字符串表示监听所有可用的网络接口
#
# # 创建 HTTP 服务器
# httpd = HTTPServer(server_address, MyHTTPRequestHandler)
#
# # 开启 HTTP 服务器，直到按下 Ctrl+C 终止
# print('Starting HTTP server on port 8181...')
# httpd.serve_forever()
