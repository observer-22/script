import re
import time
import hashlib
import pathlib

import requests

from concurrent.futures.thread import ThreadPoolExecutor


def enum(**named_values):
    return type('Enum', (), named_values)


BASE_URL = dict(baidu='https://image.baidu.com/search/acjson',
                sina='https://s.weibo.com/ajax_pic/list',
                bing="https://cn.bing.com/images/async",
                sogou="https://pic.sogou.com/pics",
                china_search="http://image.chinaso.com/getpic"
                )


class PicBase(object):

    def __init__(self, save_image_path, base_url):
        self.s = requests.Session()
        self.base_url = base_url
        self.save_path = save_image_path

    def query(self, query_topic, all_num=10):
        param_item = self.generator_image_page(all_num, query_topic)
        for param in param_item:
            flag = self.deal_image_info(param)
            if flag:
                break

    def deal_image_info(self, param):
        resp = self.s.get(self.base_url, headers={}, params=param, verify=False, timeout=10)
        resp_code = resp.status_code
        if resp_code != 200:
            return True
        image_url = self.parse_image_url(resp)
        with ThreadPoolExecutor(max_workers=20) as t:
            for url in image_url:
                t.submit(self.download_image, url)
        return False

    @classmethod
    def parse_image_url(cls, resp):
        pass
        return []

    def generator_image_page(self, all_num, query_topic):
        pass
        return []

    @classmethod
    def make_file_name(cls, url):
        m = hashlib.md5()
        m.update(url.encode())
        name = m.hexdigest()
        return name

    def download_image(self, url):
        resp = self.s.get(url, verify=False, timeout=10)
        if resp.status_code == 200:
            file_name = self.make_file_name(url)
            save_image_path = pathlib.Path(self.save_path).joinpath(file_name)
            with open(f'{str(save_image_path)}.jpg', 'wb') as f:
                f.write(resp.content)


class Sina(PicBase):

    @classmethod
    def parse_image_url(cls, resp):
        resp_json = resp.json()
        pic_list = resp_json["data"]["pic_list"]
        if pic_list and len(pic_list) > 0:
            img_links = ["http:{}".format(pic.get("original_pic")) for pic in pic_list]
            return img_links

    @classmethod
    def generator_image_page(cls, all_num, query_topic):
        page_next = 0
        for i in range(1, all_num):
            page_next += 1
            param = {'q': query_topic,
                     'page': page_next,
                     '_t': 'resultjson_com',
                     '_rnd': str(time.time())[:18],

                     }
            yield param


class BaiDu(PicBase):

    @classmethod
    def parse_image_url(cls, resp):
        img_links = re.findall(r'thumbURL.*?(https:.*?jpg)', resp.text)
        return img_links

    @classmethod
    def generator_image_page(cls, all_num, query_topic):
        page_next = 0
        for i in range(1, all_num):
            page_next = page_next + i * 48
            param = {'word': query_topic,
                     'pn': page_next,
                     'tn': 'resultjson_com',
                     'ipn': 'rj',
                     'rn': 60
                     }
            yield param


class SoGou(PicBase):

    @classmethod
    def parse_image_url(cls, resp):
        items = resp.json().get("items", [])
        for image in items:
            image_url = image.get("ori_pic_url")
            yield image_url

    @classmethod
    def generator_image_page(cls, all_num, query_topic):
        page_next = 0
        for i in range(1, all_num):
            page_next = page_next + i * 48
            param = {
                "query": query_topic,
                "mode": "1",
                "start": page_next,
                "reqType": "ajax",
                "reqFrom": "result",
                "tn": ""
            }
            yield param


class Bing(PicBase):

    @classmethod
    def parse_image_url(cls, resp):
        img_links = re.findall(r'(http.*?jpg)', resp.text)
        return img_links

    @classmethod
    def generator_image_page(cls, all_num, query_topic):
        page_next = 0
        for i in range(1, all_num):
            page_next = page_next + i * 48
            param = {'q': query_topic,
                     'first': page_next,
                     'count': 35,
                     'relp': 35,
                     'ImageBasicHover': 60
                     }
            yield param


class ChinaSearch(PicBase):

    @classmethod
    def parse_image_url(cls, resp):
        resp_json = resp.json()
        pic_list = resp_json["arrResults"]
        if pic_list and len(pic_list) > 0:
            img_links = [pic.get("url") for pic in pic_list]
            return img_links

    @classmethod
    def generator_image_page(cls, all_num, query_topic):
        page_next = 0
        for i in range(1, all_num):
            page_next += 1
            param = {'q': query_topic,
                     'st': page_next * 72,
                     'rn': '72',
                     't': str(time.time())[:18],

                     }
            yield param


if __name__ == '__main__':
    # 图片存储路径
    save_path = r"E:\bing"

    # 请求的页数
    page_num = 20

    # 查询关键字
    topic = "足球摔倒"

    WEB_CHOICE = enum(
        baidu=BaiDu(save_path, BASE_URL["baidu"]),
        sina=Sina(save_path, BASE_URL["sina"]),
        bing=Bing(save_path, BASE_URL["bing"]),
        sogou=SoGou(save_path, BASE_URL["sogou"]),
        china_search=ChinaSearch(save_path, BASE_URL["china_search"])
    )

    s = WEB_CHOICE.bing
    s.query(topic, page_num)
