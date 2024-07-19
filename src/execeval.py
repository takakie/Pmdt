import asyncio

from src.getargs import SenderParserClass
from src.senthttp import SendRequest


async def read_input(req):
    while True:
        # 异步获取用户输入
        inp = input("user:")
        if inp == "exit":
            print("Exiting input loop.")
            break
        elif inp != "":
            await req.httpRequestToCmd(cmd=inp)


async def main():
    ap = SenderParserClass()
    args = ap.parse_args()
    sr = SendRequest(args)
    await read_input(sr)


if __name__ == '__main__':
    asyncio.run(main())
