import json
import re

import time
from anaconda_project.plugins.network_util import urlparse
from bs4 import BeautifulSoup

rootUrl = "https://www.zhihu.com/"

class Parser_User(object):

    def __init__(self,session):
        self.session = session
        self.res_data = {}
        self.new_urls = set()
        self.new_search_Url = ""
    def parse(self, newUrl,userUrl,type):
        if newUrl is None :
            return
        if type == 'following':
            self.new_search_Url = "https://www.zhihu.com/api/v4/members/"+userUrl+"/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20"
        if type == 'followers':
            self.new_search_Url = "https://www.zhihu.com/api/v4/members/"+userUrl+"/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20"
        new_urls,new_data = self._get_new_data(newUrl,self.new_search_Url,type)
        return new_urls, new_data

    def _get_new_response(self,newUrl,new_Url,page):
        if page ==1:
            header = {
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
                'Host': "www.zhihu.com",
                'Origin': "http://www.zhihu.com",
                'Pragma': "no-cache",
                'Referer': newUrl,
                'X-Requested-With': "XMLHttpRequest"
            }
        else:
            newUrl_change = newUrl + "?page=" + str(page)
            header = {
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
                'Host': "www.zhihu.com",
                'Origin': "http://www.zhihu.com",
                'Pragma': "no-cache",
                'Referer':newUrl_change,
                'X-Requested-With': "XMLHttpRequest"
            }

        response = self.session.get(new_Url, headers=header)
        if response.status_code != 200:  # 这里不是调用的方法  是属性值 所以不加（）
            return None
        return json.loads(response.text)

    def _get_new_search(self,response,type,newUrl):
        if response.get('data') and response.get('data')!=None:
            for one_user in response.get('data'):
                user_name = one_user['name']
                user_url = one_user['url_token']
                user_type = one_user['user_type']
                new_url = user_type + "/" + user_url + "/"
                new_full_url = urlparse.urljoin(rootUrl, new_url)
                self.new_urls.add(new_full_url)  # 注意加“/”
                self.res_data[type + "_" + user_url] = newUrl + "," + user_name + "," + user_url
        return self.new_urls, self.res_data
    def _get_new_data(self,newUrl,new_search_Url,type):
        self.res_data = {}
        self.new_urls = set()
        response = self._get_new_response(newUrl, new_search_Url,1)
        print(response)
        if response.get('paging'):
            if response.get('paging').get('is_end') == True:
                total = response.get('paging').get('totals')
                if total<=20:
                    self.new_urls, self.res_data = self._get_new_search(response,type,newUrl)
                else:
                    offset = total//20 * 20
                    page = total//20 + 1
                    userUrl_name = response.get('paging').get('previous').split("/")[6]
                    search_lastUrl = "https://www.zhihu.com/api/v4/members/"+userUrl_name+"/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset="+str(offset)+"&limit=20"
                    last_response = self._get_new_response(newUrl, search_lastUrl,page)
                    self.new_urls, self.res_data = self._get_new_search(last_response, type, newUrl)

        if response.get('paging'):
            if response.get('paging').get('is_end') == False:
                page=1
                total = response.get('paging').get('totals')
                total_page = total//20 + 1
                searchUrl = response.get('paging').get('previous')
                start = time.time()
                while page<=total_page:
                    moreResponse = self._get_new_response(newUrl, searchUrl,page)
                    searchUrl = moreResponse.get('paging').get('next')
                    page = page + 1
                    self.new_urls, self.res_data = self._get_new_search(moreResponse, type, newUrl)
                    end = time.time()
                    if end - start >1.5:
                        time.sleep(15)

        return self.new_urls, self.res_data

