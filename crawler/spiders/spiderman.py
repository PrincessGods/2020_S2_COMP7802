from scrapy.spiders import Spider
from scrapy.selector import Selector
from crawler.items import PentestItem
from scrapy.http import Request
from scrapy import FormRequest
import re
from scrapy_splash import SplashRequest

class MySpider(Spider):
    # Usage: scrapy crawl crawler --nolog -t json -O temp/spider.json

    name = "crawler"

    def __init__(self, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.start_urls = [kwargs.get('start_urls')]
        self.allowed_domains = [kwargs.get('allowed_domains')]
        self.mode = [kwargs.get('mode')]
        self.visited_links = list()
        self.existed_form = list()
        self.dynamic = False

        if self.start_urls[0] == None:
            print("\n[Info] Please enter the start URLs of crawling. (URLs split be ' - ')")
            print("[Info] It is recommended to start with the login page if you would like to login first!")
            print("[Info] Example: http://www.google.com - http://www.packtpub.com")
            self.start_urls = input().split(" - ")

        if self.allowed_domains[0] == None:
            print("\n[Info] Please enter the allowed domains of crawling. (Domains split be ' - ')")
            print("[Info] Example: localhost:8080 - WebGoat.net - packtpub.com")
            ad = input().split(" - ")
            if ad != ['']:
                self.allowed_domains = ad
            else:
                self.allowed_domains = None

        print("\n[Info] Would you like to activate dynamic mode to crawl JavaScript contentes? (y/N)")
        print("[Info] To use dynamic mode, you must install Splash first!")
        print("[Info] Installation instruction: https://splash.readthedocs.io/en/stable/install.html")
        d_mode = input()
        if d_mode == "y" or d_mode == "Y":
            self.dynamic = True

    def start_requests(self):
        if self.dynamic:
            for u in self.start_urls:
                yield SplashRequest(u,
                                    args={'wait': 2, 'width': 1920, 'height': 1080, 'render_all': 1},
                                    callback=self.main_parse)
        else:
            for u in self.start_urls:
                yield Request(u,
                              callback=self.main_parse)

        print("\n[Info] Would you like to login an account for deep crawling? (Y/n)")
        login = input()

        if login != "n" and login != "N":
            print("[Info] Please enter your Login page URL")
            print("[Info] Example: http://localhost/example-site/login")
            loginpage = input()

            yield Request(loginpage,
                          dont_filter=True,
                          callback=self.login_parse)

    def login_parse(self, response):
        print("[Info] Please enter your user name with the input key")
        print("[Info] Example: username:admin")
        uname = input().split(":")
        print("[Info] Please enter your password with the input key")
        print("[Info] Example: password:123456")
        pwd = input().split(":")

        data = dict()
        data[uname[0]] = uname[1]
        data[pwd[0]] = pwd[1]

        if self.mode[0] == '-f':
            sele = Selector(response)
            forms = sele.xpath('//form').extract()
            link_validator = re.compile(
                "^(?:http|https):\/\/(?:[\w\.\-\+]+:{0,1}[\w\.\-\+]*@)?(?:[a-z0-9\-\.]+)(?::[0-9]+)?(?:\/|\/(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+)|\?(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+))?$")

            for form in forms:
                method = None
                action = None
                name = list()
                data1 = form.split(" ")

                for f in data1:
                    if "method=" in f:
                        method = str(f.split(">")[0].split("=")[1])[1:-1]
                    if "action=" in f:
                        action = str(f.split(">")[0].split("=")[1])[1:-1]
                    if "name=" in f:
                        name.append(str(f.split(">")[0].split("=")[1])[1:-1])

                if not link_validator.match(action):
                    action = response.urljoin(action)

                u_action = action
                for n in name:
                    u_action += n

                if u_action not in self.existed_form:
                    formInfo = PentestItem()
                    formInfo["form"] = action
                    formInfo["method"] = method
                    formInfo["name"] = name
                    formInfo["location_url"] = response.url
                    self.existed_form.append(u_action)
                    yield formInfo

        yield FormRequest.from_response(
            response,
            formdata=data,
            dont_filter=True,
            callback=self.after_login
        )

    def after_login(self, response):
        cookie1 = response.request.headers.getlist('Cookie')
        cookieInfo = PentestItem()
        cs = list()
        for c in cookie1:
            cs.append(c.decode())
        cookieInfo["cookies"] = cs
        yield cookieInfo

        if self.dynamic:
            for u in self.start_urls:
                yield SplashRequest(u,
                                    dont_filter=True,
                                    args={'wait': 2, 'width': 1920, 'height': 1080, 'render_all': 1},
                                    callback=self.main_parse)

        else:
            for u in self.start_urls:
                yield Request(u,
                              dont_filter=True,
                              callback=self.main_parse)

    def main_parse(self, response):
        sele = Selector(response)
        forms = sele.xpath('//form').extract()
        link_validator = re.compile(
            "^(?:http|https):\/\/(?:[\w\.\-\+]+:{0,1}[\w\.\-\+]*@)?(?:[a-z0-9\-\.]+)(?::[0-9]+)?(?:\/|\/(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+)|\?(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+))?$")

        for form in forms:
            method = None
            action = None
            name = list()
            data = form.split(" ")

            for f in data:
                if "method=" in f:
                    method = str(f.split(">")[0].split("=")[1])[1:-1]
                if "action=" in f:
                    action = str(f.split(">")[0].split("=")[1])[1:-1]
                if "name=" in f:
                    name.append(str(f.split(">")[0].split("=")[1])[1:-1])

            if not link_validator.match(action):
                action = response.urljoin(action)

            u_action = action
            for n in name:
                u_action += n

            if u_action not in self.existed_form:
                formInfo = PentestItem()
                formInfo["form"] = action
                formInfo["method"] = method
                formInfo["name"] = name
                formInfo["location_url"] = response.url
                self.existed_form.append(u_action)
                yield formInfo

        links = sele.xpath('//a/@href').extract()

        for link in links:
            if "logout" not in link and "log_out" not in link:
                if "?" in link:
                    if not link_validator.match(link):
                        link = response.urljoin(link)

                    method = "GET"
                    action = link.split("?")[0]
                    name = link.split("?")[1].split("&")

                    u_action = action
                    for n in name:
                        u_action += n

                    if u_action not in self.existed_form:
                        formInfo = PentestItem()
                        formInfo["form"] = action
                        formInfo["method"] = method
                        formInfo["name"] = name
                        formInfo["location_url"] = response.url
                        self.existed_form.append(u_action)
                        yield formInfo

                    continue

                if link_validator.match(link) and link not in self.visited_links:
                    self.visited_links.append(link)
                    if self.dynamic:
                        yield SplashRequest(link,
                                            args={'wait': 2, 'width': 1920, 'height': 1080, 'render_all': 1},
                                            callback=self.main_parse)
                    else:
                        yield Request(link, callback=self.main_parse)
                else:
                    full_url = response.urljoin(link)
                    if full_url not in self.visited_links and link_validator.match(full_url):
                        self.visited_links.append(full_url)
                        if self.dynamic:
                            yield SplashRequest(full_url,
                                                args={'wait': 2, 'width': 1920, 'height': 1080, 'render_all': 1},
                                                callback=self.main_parse)
                        else:
                            yield Request(full_url, callback=self.main_parse)

