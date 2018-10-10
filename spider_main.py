from douban_spider import url_manger
from douban_spider import html_downloader
from douban_spider import html_parser
from douban_spider import html_outputer

class SpiderMain(object):
    def __init__(self):
        self.urls = url_manger.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()

    def craw(self, root_url):
        count = 1
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                print('爬取第 %d 页: %s' %(count, new_url))
                html_cont = self.downloader.download(new_url)
                new_urls, new_data = self.parser.parse(new_url, html_cont)
                self.urls.add_new_urls(new_urls)
                self.outputer.collect_data(new_data)

                if count == 10:
                    break
                count = count + 1
            except:
                print('craw failed')
        self.outputer.output_html()


if __name__ == '__main__':
    str = input("请输入要下载的豆瓣相册ID(例如1639309626): ")
    root_url = 'https://www.douban.com/photos/album/'+str+'/'
    print('即将开始下载相册： %s ' % root_url)
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)