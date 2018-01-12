# coding:utf-8
import ConfigParser
import cookielib
import urllib
import urllib2
import os
from scrapy.selector import Selector
from PIL import Image
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class WeiboCookie:

    def __init__(self):
        # 定义属于自己的opener,获取记录在登陆过程中返还的cookie
        self.cookie = cookielib.CookieJar()
        self.opener = urllib2.build_opener(
            urllib2.HTTPCookieProcessor(self.cookie))
        # 注意这里只能使用旧版本的浏览器，新版本的会一只出现验证码错误，别问我怎么知道的。。〒_〒
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"}

        # 存储本地微博账号密码
        self.weibos = []
        # 存储cookie
        self.cookies = []

        # 将自定义的opener与urllib2绑定到一起
        urllib2.install_opener(self.opener)

        # 获取本地微博账号密码
        cf = ConfigParser.ConfigParser()
        cf.readfp(open(os.getcwd() + '/WeiboAccount.ini'))
        accountNum = int(cf.get('AccountNum', 'num'))

        for i in range(accountNum):
            username = cf.get('Account' + str(i), 'username')
            password = cf.get('Account' + str(i), 'password')
            self.weibos.append({'no': username, 'psw': password})

    def processCookie(self):
        dict = {}
        for c in self.cookie:
            dict[c.name] = c.value
        self.cookies.append(dict)

    def getCookie(self):
        for elem in self.weibos:
            try:
                postDataUrl = 'https://weibo.cn/login/'
                request = urllib2.Request(
                    url=postDataUrl, headers=self.headers)
                response = urllib2.urlopen(request)
                selector = Selector(text=response.read())
                postData = {}
                rand = selector.xpath(
                    'body/div/form/@action').extract()[0].split('&')[0]
                postDataUrl = postDataUrl + rand + \
                    '&backURL=http%3A%2F%2Fweibo.cn&backTitle=%E6%89%8B%E6%9C%BA%E6%96%B0%E6%B5%AA%E7%BD%91&vt=4'
                postData['remember'] = 'on'
                postData['submit'] = u'\u767b\u5f55'  # 登录
                postData['backURL'] = selector.xpath(
                    'body/div/form/div/input[@name="backURL"]/@value').extract()[0]
                postData['vk'] = selector.xpath(
                    'body/div/form/div/input[@name="vk"]/@value').extract()[0]
                postData['backTitle'] = selector.xpath(
                    'body/div/form/div/input[@name="backTitle"]/@value').extract()[0]
                postData['tryCount'] = selector.xpath(
                    'body/div/form/div/input[@name="tryCount"]/@value').extract()[0]
                postData['capId'] = selector.xpath(
                    'body/div/form/div/input[@name="capId"]/@value').extract()[0]
                postData['mobile'] = elem['no']
                passwordParameter = 'password_' + postData['vk'].split('_')[0]
                postData[passwordParameter] = elem['psw']

                # 获取验证码
                captchaUrl = selector.xpath(
                    'body/div/form/div/img/@src').extract()[0]
                postData['code'] = self.getCaptcha(captchaUrl)

                postData = urllib.urlencode(postData).encode('utf-8')
                req = urllib2.Request(url=postDataUrl,
                                      data=postData,
                                      headers=self.headers)
                # 如果一切正常的话,这个post会返回空,url会立即失效
                # 如果有错误的话,这个post会返回错误信息
                try:
                    response = urllib2.urlopen(req)
                    if (response.getcode() == 200):
                        print elem['no'], '\'s cookie receive failed'
                        print 'please check your input captcha'
                except urllib2.URLError as e:
                    if hasattr(e, 'code') and e.code == 404:
                        print elem['no'], '\'s cookie has received'
                        self.processCookie()
                    else:
                        print elem['no'], '\'s cookie receive failed'
                        print 'Reason:', e.reason
                finally:
                    if response:
                        response.close()
            except Exception as e:
                print e

    def getCaptcha(self, captchaUrl):
        request = urllib2.Request(url=captchaUrl, headers=self.headers)
        response = urllib2.urlopen(request)
        content = response.read()
        file_path = "captcha.jpg"
        local_pic = open(file_path, "wb")
        local_pic.write(content)
        local_pic.close()
        img = Image.open(file_path)
        img.show()
        captcha = raw_input('请输入验证码:\n')
        return captcha

    def updateCookie(self):
        self.getCookie()
        print 'totally get %d cookies' % len(self.cookies)
        cf = ConfigParser.ConfigParser()
        cf.add_section("cookie")
        cf.set("cookie", "num", len(self.cookies))
        for i in range(len(self.cookies)):
            cf.set("cookie", "cookie" + str(i), self.cookies[i])
        cf.write(open(os.getcwd() + '/CookieConfig.ini', 'r+'))

    @staticmethod
    def supplyCookie():
        cf = ConfigParser.ConfigParser()
        cf.readfp(open('CookieConfig/CookieConfig.ini'))
        cookies = []
        num = int(cf.get('cookie', 'num'))
        for i in range(num):
            # eval的作用是把字符串转成字典
            cookies.append(eval(cf.get('cookie', 'cookie' + str(i))))
        return cookies


if __name__ == '__main__':
    wc = WeiboCookie()
    wc.updateCookie()
    # print WeiboCookie.supplyCookie()
