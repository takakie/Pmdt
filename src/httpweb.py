import base64
import os

from aiohttp import web
from datetime import datetime


class WebApplication:
    def __init__(self, args):
        self.args = args
        self.time = datetime.now()

    async def handle_post(self, request):
        url_path = request.path
        print(url_path)
        data = await request.post()
        cmd = data.get('CMD') if data.get('CMD') else ''
        host = data.get('HOST') if data.get('HOST') else ''
        echo = data.get('ECHO') if data.get('ECHO') else ''
        print(f'============================HOST:{host}===============================')
        print("TIME: ", datetime.now())
        print("CMD:  " + str(cmd))
        print("------------------------------------------------------------------------------------")
        print("ECHO:\n" + str(echo))
        print("====================================================================================")

        return web.Response(text="success")

    async def handle_get(self, request):
        tail = request.match_info.get('tail', '')
        if not tail:
            return web.Response(text="success")
        text = base64.b64decode(tail).decode('utf-8')
        if datetime.now().timestamp() - self.time.timestamp() > 1:
            print("====================================================================================")
            print("TIME: ", datetime.now())
            print("ECHO: ")
            print("------------------------------------------------------------------------------------")
            print(text, end='')
        else:
            print(text, end='')
        self.time = datetime.now()
        if len(tail) != 76:
            print("=====================================================================================")
        return web.Response(text="success")

    async def handle_upload(self, request):
        reader = await request.multipart()
        field = await reader.next()
        assert field.name == 'file'
        filename = field.filename
        upload_dir = './uploads'  # 设置保存文件的目录
        os.makedirs(upload_dir, exist_ok=True)  # 确保目录存在，如果不存在则创建
        file_path = os.path.join(upload_dir, filename)
        with open(file_path, 'wb') as f:
            while True:
                chunk = await field.read_chunk()  # 8192 bytes by default.
                if not chunk:
                    break
                f.write(chunk)
        print(f'File {filename} has been saved to {file_path}')
        return web.Response(text=f'File {filename} has been saved to {file_path}')

    async def handle_download(self, request):
        path = request.match_info.get('path', '')
        print("Upload File: ", path)
        try:
            with open(path, 'rb') as f:
                return web.Response(body=f.read())
        except FileNotFoundError:
            return web.Response(status=404)

    def init_app(self):
        app = web.Application()
        app.router.add_get('/file/{path:.*}', self.handle_download)
        app.router.add_get('/{tail:.*}', self.handle_get)
        app.router.add_post('/upload', self.handle_upload)
        app.router.add_post('/', self.handle_post)
        return app


