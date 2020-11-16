# 导入所需的库

import json
from lxml import etree
import requests
import xlwt
import time

"""
贵阳租房数据爬取
"""


class Renting:
    # 1.初始化url和headers（请求头）
    def __init__(self):
        self.start_url = 'https://guiyang.leyoujia.com/zf/?n={}'
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}  # 获取请求头

    # 2.得到全部的URL地址
    def get_url_list(self):
        url_list = [self.start_url.format(i) for i in range(101)]  # 构造URL地址的列表形式并返回
        return url_list

    # 3.发送请求，获取相应体
    def parse_url(self, url):
        print("parsing...", url)  # 检查是否能进网站
        response = requests.get(url=url, headers=self.headers)
        return response.content.decode('utf-8', 'ignore')  # 返回解析内容

    # 4.获取数据
    def get_content_list(self, html_str):
        html = etree.HTML(html_str)
        div_list = html.xpath("/html/body/div[3]/div[2]/div[1]/div[5]/ul/li")

        content_list = []
        for div in div_list:
            items = {"布局": "", "面向": "", "建筑面积": "", "室内面积": "",
                     "装修": "", "楼层": "", "建成时间": "", "房名": "", "地区": "",
                     "地址": "", "租法": "", "价格": ""}

            items["布局"] = div.xpath(".//div[2]/p[2]/span[1]/text()")
            items["面向"] = div.xpath(".//div[2]/p[2]/span[2]/text()")
            items["建筑面积"] = div.xpath(".//div[2]/p[2]/span[3]/text()")
            items["室内面积"] = div.xpath(".//div[2]/p[2]/span[4]/text()")

            items["装修"] = div.xpath(".//div[2]/p[3]/span[1]/text()")
            items["楼层"] = div.xpath(".//div[2]/p[3]/span[2]/text()")
            items["建成时间"] = div.xpath(".//div[2]/p[3]/span[3]/text()")

            items["房名"] = div.xpath(".//div[2]/p[4]/span[1]/a/text()")
            items["地区"] = div.xpath(".//div[2]/p[4]/span[2]/a[1]/text()")
            items["地址"] = div.xpath(".//div[2]/p[4]/span[2]/a[2]/text()")

            items["价格"] = div.xpath(".//div[3]/p[1]/span/text()")
            items["租法"] = div.xpath(".//div[3]/p[2]/text()")

            content_list.append(items)
        return content_list

    # 5.保存数据
    def save_content_list(self, content_list):
        with open("guiyangzufang.txt", 'a', encoding='utf-8') as f:
            for content in content_list:
                f.write(json.dumps(content))
                f.write('\n')

    # 6.数据保存到Excel表中，利用xlwt库
    def save_to_excl(self, content_list):
        workbook = xlwt.Workbook(encoding='utf-8')
        sheet = workbook.add_sheet('guiyangzufang')
        head = ["房名", "布局", "面向", "建筑面积", "室内面积", "装修", "楼层",
                "建成时间", "地区", "地址", "价格", "租法"]

        for h in range(len(head)):
            sheet.write(0, h, head[h])

        length = len(content_list)
        for j in range(1, length + 1):
            sheet.write(j, 0, content_list[j - 1]["房名"])
            sheet.write(j, 1, content_list[j - 1]["布局"])
            sheet.write(j, 2, content_list[j - 1]["面向"])

            sheet.write(j, 3, content_list[j - 1]["建筑面积"])
            sheet.write(j, 4, content_list[j - 1]["室内面积"])
            sheet.write(j, 5, content_list[j - 1]["装修"])
            sheet.write(j, 6, content_list[j - 1]["楼层"])
            sheet.write(j, 7, content_list[j - 1]["建成时间"])
            sheet.write(j, 8, content_list[j - 1]["地区"])
            sheet.write(j, 9, content_list[j - 1]["地址"])
            sheet.write(j, 10, content_list[j - 1]["价格"])
            sheet.write(j, 11, content_list[j - 1]["租法"])

        workbook.save("./guiyangzufang.xls")

    def main(self):
        # 获取url_list
        url_list = self.get_url_list()
        content_lists = []
        # 在url_list中进行请求的发送，内容的获取以及保存数据
        for url in url_list:
            html_str = self.parse_url(url)
            content_list = self.get_content_list(html_str)
            self.save_content_list(content_list)  # 保存content_list
            content_lists.extend(content_list)  # 将所有的content_list全部追加到content_lists
        self.save_to_excl(content_lists)  # 保存到Excel中


if __name__ == '__main__':
    time.sleep(1)
    guiyang = Renting()
    guiyang.main()
