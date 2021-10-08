import requests
from lxml import html
etree = html.etree

class Pc:
    def pc(self,url,xpath_path):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36'

        }
        page_text = requests.get(url, headers=headers).text
        tree = etree.HTML(page_text)
        li_list = tree.xpath(xpath_path)
        return li_list