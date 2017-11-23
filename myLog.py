import json
import re
from getpass import getpass

import requests
import time
global session
header = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36",
    'Host': "www.zhihu.com",
    'Origin': "http://www.zhihu.com",
    'Pragma': "no-cache",
    'Referer': "http://www.zhihu.com/",
    'X-Requested-With': "XMLHttpRequest"
}
session = requests.session()

def search_xsrf():
    response = session.get('https://www.zhihu.com/',headers = header)
    results = re.match('[\s\S]*name="_xsrf" value="(.*?)"',response.text)
    if results:
        return results.group(1)
    return ''
def down_captha():
    captha_url = 'https://www.zhihu.com/captcha.gif?r=%d&type=login&lang=cn' % (int(time.time()*1000))
    response = session.get(captha_url,headers=header)
    with open('captcha.gif','wb') as f:
        f.write(response.content)
        f.close()

    from PIL import Image
    try:
        img = Image.open('captcha.gif')
        img.show()
        img.close()
    except:
        pass

    captcha = {
        'img_size':[200,44],
        'input_points':[],
    }
    points = [[16.875, 28], [32.875, 27], [65.875, 31], [88.875, 24], [106.875, 24], [147.875, 30],
              [174.875, 29]]
    seq = input('请输入倒立字的位置\n>')
    for i in seq:
        captcha['input_points'].append(points[int(i)-1])
    return json.dumps(captcha)#因为本身是json格式的

def zhihu_Login(account=None,password=None):
    if account == None:
        print("请输入账户")
        account = input()
        print("请输入密码")
        #password = getpass("请输入密码:")
        password = input()
    if re.match('1\d{10}',account):
        print("手机号登录")
        post_url='https://www.zhihu.com/login/phone_num'
        post_form={
            '_xsrf':search_xsrf(),
            'password':password,
            'captcha':down_captha(),
            'captcha_type':'cn',
            'phone_num':account
        }
        response_text = session.post(post_url,data=post_form,headers=header,allow_redirects=False)
        response_text = json.loads(response_text.text)
        if 'msg' in response_text and response_text['msg'] == '登录成功':
            print("登录成功")
        else:
            print("登录失败,请重新登录")
            zhihu_Login()


# if __name__=='__main__':
#     header={
#         'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36",
#         'Host': "www.zhihu.com",
#         'Origin': "http://www.zhihu.com",
#         'Pragma': "no-cache",
#         'Referer': "http://www.zhihu.com/",
#         'X-Requested-With': "XMLHttpRequest"
#     }
#     session=requests.session()
#     zhihu_Login()