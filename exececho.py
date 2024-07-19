import asyncio
from src.getargs import SenderParserClass
from src.httpweb import WebApplication
from aiohttp import web
from src.senthttp import SendRequest


async def read_input(loop, listenerIP, port):
    while True:
        # 异步获取用户输入
        inp = await loop.run_in_executor(None, input, "root: ")
        print(f"Received input: {inp}")
        if inp == "exit":
            print("Exiting input loop.")
            break
        elif inp != "":
            sr = SendRequest(listenerIP, port)
            await sr.httpRequestToCmd(cmd=inp)
            await asyncio.sleep(3)


async def main():
    ap = SenderParserClass()
    args = ap.parse_args()
    wa = WebApplication(args)
    loop = asyncio.get_running_loop()

    # 创建服务器和输入任务
    app = await wa.init_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', args.port)
    await site.start()

    print(f'Server started at http://{args.listenerIP}:{args.port}')
    input_task = loop.create_task(read_input(loop, args.listenerIP, args.port))

    try:
        # 等待输入任务结束
        await input_task
    finally:
        # 关闭服务器
        await runner.cleanup()


if __name__ == '__main__':
    asyncio.run(main())
