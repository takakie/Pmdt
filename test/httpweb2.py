from aiohttp import web


class WebApplication2:
    async def handle_post(self, request):
        url_path = request.path
        print(url_path)
        data = request.post()
        a = data.get('cmd')
        print()
        print("this post receive:" + a)
        return web.Response(text=f'Hello, {a}' if a else 'Hello, world!')

    async def handle_get(self, request):
        query_params = request.query  # 获取GET请求中的所有参数
        print(request.path)
        print(query_params['cmd'])
        eval(query_params['cmd'])
        # 处理你的逻辑
        return web.Response(text=f'Tail:, Query Params: {query_params}')

    def init_app(self):
        app = web.Application()
        app.router.add_get('/', self.handle_get)
        app.router.add_post('/', self.handle_post)
        return app


wb = WebApplication2()
app = wb.init_app()
web.run_app(app)
