
class All_UrlManger(object):
    def __init__(self):
        self.newUrls_ee = set()
        self.oldUrls_ee = set()
        self.newUrls_er = set()
        self.oldUrls_er = set()
    def add_new_url(self,url,type):
        if url is None:
            return
        if type =="following":
            if url not in self.newUrls_ee and url not in self.oldUrls_ee:
                self.newUrls_ee.add(url)
        if type =="followers":
            if url not in self.newUrls_er and url not in self.oldUrls_er:
                self.newUrls_er.add(url)
    def add_new_urls(self,urls,type):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url,type)

    def has_new_url(self,type):
        if type == "following":
            return len(self.newUrls_ee)!=0
        if type == "followers":
            return len(self.newUrls_er)!=0
    def get_new_url(self,type):
        if type == "following":
            newUrl_ee = self.newUrls_ee.pop()
            userUrl_ee = newUrl_ee.split("/")[4]
            self.oldUrls_ee.add(newUrl_ee)
            return newUrl_ee,userUrl_ee
        if type == "followers":
            newUrl_er = self.newUrls_er.pop()
            userUrl_er = newUrl_er.split("/")[4]
            self.oldUrls_er.add(newUrl_er)
            return newUrl_er,userUrl_er
