from bs4 import BeautifulSoup
import re
import urllib.parse
import urllib.request

class HtmlParser(object):
    def _get_new_urls(self,page_url,soup):

        new_urls = set()

        links = soup.find_all('img',width="201")
        for link in links:
            photo_url = link['src']
            photo_url_list = list(photo_url)
            photo_url_list[37] = 'l'               #将列表中的第37个字符修改为l，从而将图片修改为大图
            photo_url = ''.join(photo_url_list)      #用空字符串将列表中的所有字符重新连接为字符串

            photo_name = photo_url[46:57] #取出连接中的图片名称
            print('正在下载图片：%s.jpg'% photo_name)

            urllib.request.urlretrieve(photo_url, 'photo/%s.jpg' % photo_name)


        pages = soup.find_all('a', href=re.compile(r'https://www.douban.com/photos/album/\w*/\?start'))
        for link in pages:
            new_url = link['href']
            new_full_url = urllib.parse.urljoin(page_url, new_url)
            new_urls.add(new_full_url)
        return new_urls

    def _get_new_data(self,page_url,soup):
        res_data={}
        res_data['url'] = page_url
        return res_data

    def parse(self,page_url,html_cont):
        if page_url is None or len(html_cont)==0 :
            return None
        soup = BeautifulSoup(html_cont,'html.parser',from_encoding='iso-8859-1')
        #from_encoding='iso-8859-1'
        new_urls = self._get_new_urls(page_url,soup)
        new_data = self._get_new_data(page_url,soup)
        return new_urls,new_data