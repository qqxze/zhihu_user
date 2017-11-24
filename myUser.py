import json

import requests
import time

from zhihuAnyls import output, myLog, pares_zhihu_user,  AllManger


class User(object):
    def __init__(self,session):
        # self.urls = manger.UrlManger()
        # self.urls_er = manger_er.UrlManger_er()
        self.all_urls = AllManger.All_UrlManger()
        self.parser = pares_zhihu_user.Parser_User(session)
        self.outputer = output.HtmlOutputer()
        #self.outputer_er = output_er.HtmlOutputer_er()
        self.session = session
        self.header = {
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36",
        'Host': "www.zhihu.com",
        'Origin': "http://www.zhihu.com",
        'Pragma': "no-cache",
        'Referer': "https://www.zhihu.com/people/zhu-zhu-82-13",
        'X-Requested-With': "XMLHttpRequest"
    }

    # def get_pageUrl(self,pageurl):
    #     response = self.session.get(pageurl,headers = self.header)
    #     if response.status_code != 200:#这里不是调用的方法  是属性值 所以不加（）
    #        return  None
    #     return response.text#返回整个html json.dumps是将json格式转为字符串格式

    def following(self,root_url):
        count = 1
        type = "following"
        self.all_urls.add_new_url(root_url, type)
        while self.all_urls.has_new_url(type):
            # try:
            newUrl_ee,userUrl_ee = self.all_urls.get_new_url(type)
            if count>1:
                self.followers(newUrl_ee)
            print('craw_following %d : %s' % (count, newUrl_ee))
            newUrls_following,newData_following = self.parser.parse(newUrl_ee, userUrl_ee, type)
            print(newUrls_following)
            print(newData_following)
            self.all_urls.add_new_urls(newUrls_following, type)
            self.outputer.collect_data(newData_following, type)
            if count == 2:
                break
            count = count + 1
            # except:
            #     print("craw failed")
        self.outputer.output_csv("following.csv", type)


    def followers(self,root_url):

        count = 1
        type = 'followers'
        self.all_urls.add_new_url(root_url,type)
        while self.all_urls.has_new_url(type):
            # try:
            start = time.time()
            newUrl_er,userUrl_er = self.all_urls.get_new_url(type)
            print('craw_follower %d : %s' % (count, newUrl_er))
            newUrls_er,newData_er = self.parser.parse(newUrl_er,userUrl_er,type)
            print(newUrls_er)
            print(newData_er)
            self.all_urls.add_new_urls(newUrls_er,type)
            self.outputer.collect_data(newData_er,type)
            if count == 2:
                break
            count = count + 1
            end = time.time()
            if end-start > 2:
                time.sleep(5)
            # except:
            #     print("craw failed")
        self.outputer.output_csv("followers.csv",type)

if __name__=='__main__':
    myLog.zhihu_Login()
    session = myLog.session
    print("spider")
    root_url = 'https://www.zhihu.com/people/zhu-zhu-82-13/'
    root_url1="https://www.zhihu.com/people/zhang-william-38/"
    user_craw = User(session)
    user_craw.following(root_url)
    #user_craw.followers(root_url1)
