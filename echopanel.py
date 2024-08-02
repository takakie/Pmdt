from src.getargs import ListenerParserClass
from src.httpweb import WebApplication
from aiohttp import web


def main():
    ap = ListenerParserClass()
    args = ap.parse_args()
    wb = WebApplication(args)
    app = wb.init_app()
    web.run_app(app, port=args.port)


if __name__ == '__main__':
    main()
