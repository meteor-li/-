from django.shortcuts import render,HttpResponse
import re
import requests
import time
import json
from bs4 import BeautifulSoup
CTIME = None
QCODE = None
TIPS = 1
Ticket_dict = {}
USER_INFO_DICT = {}
ALL_COOKIE = {}
def Login(request):
    global CTIME
    CTIME = time.time()
    url = 'https://login.wx.qq.com/jslogin?appid=wx782c26e4c19acffb&fun=new&lang=zh_CN&_=%s'%CTIME
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6726.400 QQBrowser/10.2.2265.400'
    }
    # 向腾讯发送请求，获得登录的二维码
    response = requests.get(url=url,headers=headers)
    v = re.findall('uuid = "(.*)";',response.text)
    global QCODE
    QCODE = v[0]
    return render(request,'app/login.html',{'qrcode':QCODE})

def check_login(request):
    global TIPS
    ret = {'code':408,'data':None}
    url = 'https://login.wx.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid=%s&tip=%s&r=989866995&_=%s'%(QCODE,TIPS,CTIME)
    # 向腾讯服务器发送请求，获得扫码用户的头像
    r1 = requests.get(url=url)
    # 间隔时间过长，无人扫码返回408
    if 'window.code=408' in r1.text:
        print('无人扫码')
        return HttpResponse(json.dumps(ret))
    # 微信扫码，返回201同时返回加密的用户头像
    elif 'window.code=201' in r1.text:
        ret['code'] = 201
        TIPS = 0
        v = re.findall("window.userAvatar = '(.*)';",r1.text)[0]
        ret['data'] = v
        # 获得用户头像并返回给登录页面，替换二维码图片
        return HttpResponse(json.dumps(ret))
    # 用户在手机上同意登录网页微信，返回200同时返回登录信息
    elif 'window.code=200' in r1.text:
        ret['code'] = 200
        # 获取用户的登陆请求的url
        redirect_uri = re.findall('window.redirect_uri="(.*)";',r1.text)[0]
        redirect_uri = redirect_uri + '&fun=new&version=v2&lang=zh_CN'

        r2 = requests.get(url=redirect_uri)
        # 存储cookies
        ALL_COOKIE.update(r1.cookies.get_dict())
        ALL_COOKIE.update(r2.cookies.get_dict())
        # 获取登录凭证（表单传递的值）
        soup = BeautifulSoup(r2.text,'lxml')
        for tag in soup.find('error').children:
            Ticket_dict[tag.name] = tag.get_text()
        # 获取登录信息
        # redirect_uri_dict = {
        #     'BaseRequest':{
        #         'DeviceID':"e095808275553167",
        #         'Sid':Ticket_dict['wxsid'],
        #         'Uin':Ticket_dict['wxuin'],
        #         'Skey':Ticket_dict['skey'],
        #     }
        # }
        # get_userinfo = 'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxinit?r=976385395&lang=zh_CN&pass_ticket=' + Ticket_dict['pass_ticket']
        # r3 = requests.post(url=get_userinfo,json=redirect_uri_dict)
        # # 获取用户信息
        # r3.encoding = 'utf-8'
        # user_info = json.loads(r3.text)
        # contact_list = user_info['ContactList']
        # for item in contact_list:
        #     # 打印取出的用户信息（只有最近的活跃的用户）
        #     print(item['PYQuanPin'],item['NickName'])
        return HttpResponse(json.dumps(ret))

def user(request):
    """
    个人主页
    """
    redirect_uri_dict = {
        'BaseRequest': {
            'DeviceID': "e095808275553167",
            'Sid': Ticket_dict['wxsid'],
            'Uin': Ticket_dict['wxuin'],
            'Skey': Ticket_dict['skey'],
        }
    }
    get_userinfo = 'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxinit?r=976385395&lang=zh_CN&pass_ticket=' + Ticket_dict[
        'pass_ticket']
    r3 = requests.post(url=get_userinfo, json=redirect_uri_dict)
    ALL_COOKIE.update(r3.cookies.get_dict())
    # 获取用户信息
    r3.encoding = 'utf-8'
    user_info = json.loads(r3.text)
    USER_INFO_DICT.update(user_info)
    print(USER_INFO_DICT['User']['UserName'])
    # print(user_info)
    # for k,v in user_info.items():
    #     #     print(k,v)
    return render(request,'app/user.html',{'user_info':user_info})

def contact_list(request):
    """
    获取更多联系人，并在页面中显示
    :param request:
    :return:
    """
    url = 'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxgetcontact?pass_ticket=%s&r=%s&seq=0&skey=%s'%(Ticket_dict['pass_ticket'],CTIME,Ticket_dict['skey'])
    reponse = requests.get(url=url,cookies=ALL_COOKIE)
    reponse.encoding = 'utf-8'
    contact_list = json.loads(reponse.text)
    return render(request,'app/contact-list.html',{'contact_list':contact_list})

def sendmsg(request):
    '''
    发送消息
    '''
    touser = request.GET.get('toUser')
    msg = request.GET.get('msg')
    print(touser)
    url = 'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxsendmsg?lang=zh_CN&pass_ticket=%s'%Ticket_dict['pass_ticket']
    post_dict = {
        'BaseRequest': {
            'DeviceID': "e095808275553167",
            'Sid': Ticket_dict['wxsid'],
            'Uin': Ticket_dict['wxuin'],
            'Skey': Ticket_dict['skey'],
        },
        'Msg':{
            'ClientMsgId':CTIME,
            'Content':msg,
            'FromUserName':USER_INFO_DICT['User']['UserName'],
            'LocalID':CTIME,
            'ToUserName':touser.strip(),
            'Type': 1,
        },
        'Scene':0,
    }
    # response = requests.post(url=url,json=post_dict,cookies=ALL_COOKIE)
    response = requests.post(url=url,data=bytes(json.dumps(post_dict,ensure_ascii=False),encoding='utf-8'))
    print(response.text)
    return HttpResponse('ok')

def getmsg(request):
    '''接收消息
    检查是否有消息发过来
     如果有消息到来则访问URL获取消息
    '''
    synckey_list = USER_INFO_DICT['SyncKey']['List']
    sync_list = []
    post_dict = {
        'BaseRequest': {
            'DeviceID': "e095808275553167",
            'Sid': Ticket_dict['wxsid'],
            'Uin': Ticket_dict['wxuin'],
            'Skey': Ticket_dict['skey'],
        },
        'SyncKey':USER_INFO_DICT['SyncKey'],
        'Scene':0,
        'rr':1,
    }
    for item in synckey_list:
        temp = "%s_%s"%(item['Key'],item['Val'])
        sync_list.append(temp)
        SyncKey = "|".join(sync_list)
    url = 'https://wx.qq.com/cgi-bin/mmwebwx-bin/synccheck'
    response = requests.get(url=url,params={
                'r':CTIME,
                'skey':Ticket_dict['skey'],
                'sid':Ticket_dict['wxsid'],
                'uin':Ticket_dict['wxwin'],
                'deviceid':'e095808275553167',
                'synckey':SyncKey,},cookies=ALL_COOKIE)
    if 'retcode:"0",selector:"2"' in response.text:
        r2=requests.post(
            url='https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxsync',
            params={
                'skey': Ticket_dict['skey'],
                'sid': Ticket_dict['wxsid'],
                'pass_ticket':Ticket_dict['pass_ticket'],
                'lang-zh':'zh_CN',
            },json=post_dict,cookies=ALL_COOKIE)
        r2.encoding='utf-8'
        msg_dict = json.loads(r2.text)
        for msg in msg_dict['AddMsgList']:
            print(msg['Content'])

        USER_INFO_DICT['SyncKey']=msg_dict['SyncKey']
    return HttpResponse('...')