# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import reply
import receive
import web
import json
import requests

def get_access_token():

    url = 'https://api.weixin.qq.com/cgi-bin/token'
    params = {'grant_type': 'client_credential', 'appid': 'wx17fdb6fbf2166ff5', 'secret': '87bb3b2b1ba667148b98bed8b786a796'}

    print(111111111)
    r = requests.get(url, params=params)
    print(r.text)

    data = json.loads(r.text)
    print('Get New Access Token: ' + data['access_token'])
    return data['access_token']

def getjson_testdata(key):
    with open('testdata.json', 'r') as f:
        load_dict = json.load(f)
        return load_dict[key]

def getjson_news():
    with open('news.json', 'r') as f:
        news = json.load(f)
        content = ''
        for i in news:
            title = news[i]['title'].encode('utf-8')
            url = news[i]['url'].encode('utf-8')
            content = content + title + url + '\n'
        return content

def reply_text(toUser, fromUser, content):
    replyMsg = reply.TextMsg(toUser, fromUser, content)
    return replyMsg.send()

def reply_image(toUser, fromUser, filename):
    mediaId = upload_temp_image(filename)
    # mediaId = recMsg.MediaId
    replyMsg = reply.ImageMsg(toUser, fromUser, mediaId)
    return replyMsg.send()

def upload_temp_image(filename):
    token = get_access_token()
    print(token)
    url = 'https://api.weixin.qq.com/cgi-bin/media/upload'

    file = open(filename, 'rb')
    params = {'access_token': token, 'type': 'image'}
    files = {'media': file}

    r = requests.post(url, params=params, files=files)
    #print(r.text)
    mediaId = json.loads(r.text)['media_id']

    return mediaId

class Handle(object):
    def POST(self):
        try:
            webData = web.data()
            print("Handle Post webdata is ", webData)
            # 后台打日志
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg):
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                if recMsg.MsgType == 'text':
                    if recMsg.Content == '门铃':
                        content = getjson_testdata('bell')
                        return reply_text(toUser, fromUser, content)
                    elif recMsg.Content == '阳台门':
                        content = getjson_testdata('door')
                        return reply_text(toUser, fromUser, content)
                    elif recMsg.Content == '气温' or recMsg.Content == '温度':
                        content = getjson_testdata('temperature')
                        return reply_text(toUser, fromUser, content)
                    elif recMsg.Content == 'pm2.5':
                        content = getjson_testdata('pm25')
                        return reply_text(toUser, fromUser, content)
                    elif recMsg.Content == '湿度':
                        content = getjson_testdata('humidity')
                        return reply_text(toUser, fromUser, content)
                    elif recMsg.Content == '新闻':
                        content = getjson_news()
                        return reply_text(toUser, fromUser, content)
                    elif recMsg.Content == '摄像头':
                        filename = 'QRcode.jpg'
                        return reply_image(toUser, fromUser, filename)
                    elif recMsg.Content == '帮助':
                        content = '输入“气温”查看实时温度\n输入“湿度”查看实时湿度\n输入“pm2.5”查看实时pm2.5\n输入“新闻”查看10条热点新闻\n' \
                                  '输入“阳台门”查看阳台门状态\n输入“摄像头”查看走廊监控画面'
                        return reply_text(toUser, fromUser, content)
                    else:
                        content = '欢迎使用智能家居系统！\n请输入“帮助”查看所有可用指令'
                        return reply_text(toUser, fromUser, content)
                #content = "zypnb"
                #replyMsg = reply.TextMsg(toUser, fromUser, content)
                #return replyMsg.send()
            else:
                print("暂且不处理")
                return "success"
        except Exception, Argment:
            return Argment

    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "LJZNBD" #请按照公众平台官网\基本配置中信息填写

            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            print("handle/GET func: hashcode, signature: ", hashcode, signature)
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception, Argument:
            return Argument
