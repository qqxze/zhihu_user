import csv


class HtmlOutputer(object):

    def __init__(self):
        self.datas_ee = []
        self.datas_er = []
    def collect_data(self,data,type):
        if data is None:
            return
        if type == "following":
            self.datas_ee.append(data)
        if type == "followers":
            self.datas_er.append(data)
    def output_csv(self,filename,type):

        with open (filename,"w",newline='') as f:
            headers = ["user_url",type+"_name",type+"_url"]
            writer = csv.writer(f)
            writer.writerow(headers)
            if type == "following":
                for data in self.datas_ee:
                    for key in data:
                        if data[key]:
                            writer.writerow([data[key].split(",")[0].split("/")[4], data[key].split(",")[1],data[key].split(",")[2]])
                        # writer.writerow([data[key].split(",")[0].split("/")[4],data[key].split(",")[1],data[key].split(",")[2].split("/")[2]])
            if type == "followers":
                for data in self.datas_er:
                    for key in data:
                        if data[key]:
                            writer.writerow([data[key].split(",")[0].split("/")[4], data[key].split(",")[1],
                                             data[key].split(",")[2]])
        f.close()
# if __name__ == "__main__":
#     str1 = {'dd':'https://www.zhihu.com/people/zhu-zhu/following,七月在夏天1,/people/qi'}
#     str={'following_七月在夏天': 'https://www.zhihu.com/people/zhu-zhu-82-13/following,七月在夏天,/people/qi_yue', 'following_阿萨姆': 'https://www.zhihu.com/people/zhu-zhu-82-13/following,阿萨姆,/people/breaknever', 'following_南瓜星人': 'https://www.zhihu.com/people/zhu-zhu-82-13/following,南瓜星人,/people/zhang-william-38'}
#     a=HtmlOutputer()
#     a.collect_data(str1)
#     a.collect_data(str)
#     a.output_csv("following")

