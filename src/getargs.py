import argparse


class RestrictedInt:
    def __init__(self, low, high):
        self.low = low
        self.high = high

    def __call__(self, value):
        ivalue = int(value)
        if ivalue < self.low or ivalue > self.high:
            raise argparse.ArgumentTypeError(f"{value} is not in range {self.low} to {self.high}")
        return ivalue


class SenderParserClass:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='This is a request sender; 这是一个请求发送器，可通过url或者请求文件进行发送请求。')
        self.parser.add_argument('listenerIP', type=str, help='This is receive IP; 监听器启动的IP地址。')
        self.parser.add_argument('-p', '--port', type=RestrictedInt(1, 65536), help='The listener listens on port number 8000 by default.; 监听器监听端口号，默认为8000。',
                                 default='8000')
        self.parser.add_argument('-m', '--method', type=str, help='Method of request echo, It is recommended to use the POST method, with the POST method being the default.; 回显请求请求方法，建议使用POST方法，默认为POST方法。',
                                 default='POST')
        self.parser.add_argument('-u', '--url', type=str, help='There is a command injection URL path, with the injection points marked by "*".; 存在命令注入的url路径，使用"*"号标注注入点。')
        self.parser.add_argument('--path', type=str, help='There is a command injection request package path, which defaults to the request.txt file under the files directory. Injection points in the file are marked with "*"; 存在命令注入的请求包路径，默认为files文件下的request.txt文件，文件中使用"*"号标注注入点。', default='../files/request.txt')

    def parse_args(self):
        return self.parser.parse_args()


class ListenerParserClass:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='This is a command echo listener; 开启一个监听面板，用于接收命令执行的回显。')
        self.parser.add_argument('-p', '--port', type=RestrictedInt(1, 65536), help='this is receive port; 监听器的接收端口。',
                                 default='8000')

    def parse_args(self):
        return self.parser.parse_args()
