from http.server import BaseHTTPRequestHandler, HTTPServer


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        # 读取请求体内容
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print("CMD ECHO:\n", post_data.decode('utf-8'))

        # 发送响应
        self.send_response(200)
        self.end_headers()
        self.wfile.write("error".encode('utf-8'))


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd server on port {port}")
    httpd.serve_forever()


if __name__ == '__main__':
    run()
