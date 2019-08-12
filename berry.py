# -*- coding: utf-8 -*-
import random
import logging
import requests
import traceback
import re

from lxml import etree


class Berry:
    def __init__(self):
        self.url= 'http://www.berrylook.com'
        self.domain= 'http://www.berrylook.com'

    def getHeader(self):
        heasers_l = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"

        ]
        h = random.choice(heasers_l)
        headers = {"User-Agent":h}
        return headers

    def getMet(self,url,params={}):
        try:
            h = self.getHeader()
            getres_ = requests.get(
                    url=url,
                    headers=h,
                    params=params,
                    timeout=120
            )
            print(url,getres_.status_code)
            return getres_
        except Exception as e:
            print(traceback.print_exc())
            logging.info(url)
            return -1

    def postMet(self,url,data={}):
        try:
            h = self.getHeader()
            getres_ = requests.post(
                    url=url,
                    headers=h,
                    data=data,
                    timeout=120
            )
            return getres_
        except Exception as e:
            print(traceback.print_exc())
            logging.info(url)
            return -1

    def homeEntry(self):
        try:
            # headers = self.getHeader()
            res_ = self.getMet(self.url)
            res_.encoding = res_.apparent_encoding
            res = res_.text
            resx = etree.HTML(res)
            return resx
        except Exception as e:
            print(traceback.print_exc())
            return -1

    def newInEntry(self):
        burls = []
        homeresx = self.homeEntry()
        newStartUrls = homeresx.xpath('/html/body/div[3]/div/div[1]/ul/li[2]/div/ul//a/@href')
        for n in newStartUrls:
            burl = self.domain+n
            burls.append(burl)
        # print(burls)
        alllis = []
        # newInUrl = 'http://www.berrylook.com/en/Sale/New-In-LandingPage'
        try:
            for burl in burls:
                # header = self.getHeader()
                newres_ = self.getMet(burl)
                newres_.encoding = newres_.apparent_encoding
                newtext = newres_.text
                newtextx = etree.HTML(newtext)
                producturls = self.newInProductUrl(newtextx)
                # print(burl,len(producturls))
                alllis = alllis + producturls
                # for p in range(2,100):
                #     header = self.getHeader()
                #     data = {
                #         'p':str(p)
                #     }
                #     newres_ = self.postMet(burl, header,data)
                #     print(p,newres_.status_code)
                #     newres_.encoding = newres_.apparent_encoding
                #     newtext = newres_.text
                #     newtextx = etree.HTML(newtext)
                #     producturls = self.newInProductUrl(newtextx)
                #     if not producturls:
                #         break
                #     else:
                #         alllis = alllis + producturls
            return alllis
        except Exception as e:
            print(traceback.print_exc())
            return -1

    def newInProductUrl(self,newtextx):
        try:
            producturls = []
            products = newtextx.xpath('//div[@class="product-item__img"]/a/@href')
            for pr in products:
                url = self.domain+pr
                producturls.append(url)
            return producturls
        except Exception as e:
            print(traceback.print_exc())
            return -1

    #dresser 连衣裙
    def dressesEntry(self):
        burls = []
        homeresx = self.homeEntry()
        newStartUrls = homeresx.xpath('/html/body/div[3]/div/div[1]/ul/li[3]/div/ul//a/@href')
        for n in newStartUrls[1:]:
            burl = self.domain+n
            burls.append(burl)
        print(burls)
        alllis = []
        try:
            for burl in burls:
                # header = self.getHeader()
                newres_ = self.getMet(burl)
                newres_.encoding = newres_.apparent_encoding
                newtext = newres_.text
                newtextx = etree.HTML(newtext)
                producturls = self.newInProductUrl(newtextx)
                print(burl,len(producturls))
                alllis = alllis + producturls

                allpagesx = newtextx.xpath('//div[@class="pagination"]/a/text()')
                if len(allpagesx) > 1:
                    allpage = int(allpagesx[-2]) + 1
                else:
                    allpage = 2
                for p in range(2,allpage):
                    # header = self.getHeader()
                    params = {
                        'p':str(p)
                    }
                    newres_ = self.getMet(burl,params)
                    newres_.encoding = newres_.apparent_encoding
                    newtext = newres_.text
                    newtextx = etree.HTML(newtext)
                    producturls = self.newInProductUrl(newtextx)
                    print(newres_.url,len(producturls))
                    if not producturls:
                        break
                    else:
                        alllis = alllis + producturls
            return alllis
        except Exception as e:
            print(traceback.print_exc())
            return -1

    #tops 4 目录
    def topsEntry(self):
        burls = []
        homeresx = self.homeEntry()
        newStartUrls = homeresx.xpath('/html/body/div[3]/div/div[1]/ul/li[4]/div/ul//a/@href')
        for n in newStartUrls[1:]:
            burl = self.domain+n
            burls.append(burl)
        print(burls)
        alllis = []
        try:
            for burl in burls:
                # header = self.getHeader()
                newres_ = self.getMet(burl)
                newres_.encoding = newres_.apparent_encoding
                newtext = newres_.text
                newtextx = etree.HTML(newtext)
                producturls = self.newInProductUrl(newtextx)
                print(burl,len(producturls))
                alllis = alllis + producturls

                allpagesx = newtextx.xpath('//div[@class="pagination"]/a/text()')
                if len(allpagesx) > 1:
                    allpage = int(allpagesx[-2]) + 1
                else:
                    allpage = 2
                for p in range(2,allpage):
                    # header = self.getHeader()
                    params = {
                        'p':str(p)
                    }
                    newres_ = self.getMet(burl,params)
                    newres_.encoding = newres_.apparent_encoding
                    newtext = newres_.text
                    newtextx = etree.HTML(newtext)
                    producturls = self.newInProductUrl(newtextx)
                    print(newres_.url,len(producturls))
                    if not producturls:
                        break
                    else:
                        alllis = alllis + producturls
            return alllis
        except Exception as e:
            print(traceback.print_exc())
            return -1

    # shose 5 鞋
    def shoesEntry(self):
        burls = []
        homeresx = self.homeEntry()
        newStartUrls = homeresx.xpath('/html/body/div[3]/div/div[1]/ul/li[5]/div/ul//a/@href')
        for n in newStartUrls[1:]:
            burl = self.domain + n
            burls.append(burl)
        print(burls)
        alllis = []
        try:
            for burl in burls:
                # header = self.getHeader()
                newres_ = self.getMet(burl)
                newres_.encoding = newres_.apparent_encoding
                newtext = newres_.text
                newtextx = etree.HTML(newtext)
                producturls = self.newInProductUrl(newtextx)
                print(burl, len(producturls))
                alllis = alllis + producturls

                allpagesx = newtextx.xpath('//div[@class="pagination"]/a/text()')
                if len(allpagesx) > 1:
                    allpage = int(allpagesx[-2]) + 1
                else:
                    allpage = 2
                for p in range(2, allpage):
                    # header = self.getHeader()
                    params = {
                        'p': str(p)
                    }
                    newres_ = self.getMet(burl, params)
                    newres_.encoding = newres_.apparent_encoding
                    newtext = newres_.text
                    newtextx = etree.HTML(newtext)
                    producturls = self.newInProductUrl(newtextx)
                    print(newres_.url, len(producturls))
                    if not producturls:
                        break
                    else:
                        alllis = alllis + producturls
            return alllis
        except Exception as e:
            print(traceback.print_exc())
            return -1

    #knitweaer 6 针织品
    def knitweaerEntry(self):
        burls = []
        homeresx = self.homeEntry()
        newStartUrls = homeresx.xpath('/html/body/div[3]/div/div[1]/ul/li[6]/div/ul//a/@href')
        for n in newStartUrls[1:]:
            burl = self.domain + n
            burls.append(burl)
        print(burls)
        alllis = []
        try:
            for burl in burls:
                # header = self.getHeader()
                newres_ = self.getMet(burl)
                newres_.encoding = newres_.apparent_encoding
                newtext = newres_.text
                newtextx = etree.HTML(newtext)
                producturls = self.newInProductUrl(newtextx)
                print(burl, len(producturls))
                alllis = alllis + producturls

                allpagesx = newtextx.xpath('//div[@class="pagination"]/a/text()')
                if len(allpagesx) > 1:
                    allpage = int(allpagesx[-2]) + 1
                else:
                    allpage = 2
                for p in range(2, allpage):
                    # header = self.getHeader()
                    params = {
                        'p': str(p)
                    }
                    newres_ = self.getMet(burl, params)
                    newres_.encoding = newres_.apparent_encoding
                    newtext = newres_.text
                    newtextx = etree.HTML(newtext)
                    producturls = self.newInProductUrl(newtextx)
                    print(newres_.url, len(producturls))
                    if not producturls:
                        break
                    else:
                        alllis = alllis + producturls
            return alllis
        except Exception as e:
            print(traceback.print_exc())
            return -1

    #outerweaer 7 外套
    def outerweaerEntry(self):
        burls = []
        homeresx = self.homeEntry()
        newStartUrls = homeresx.xpath('/html/body/div[3]/div/div[1]/ul/li[7]/div/ul//a/@href')
        for n in newStartUrls[1:]:
            burl = self.domain + n
            burls.append(burl)
        print(burls)
        alllis = []
        try:
            for burl in burls:
                # header = self.getHeader()
                newres_ = self.getMet(burl)
                newres_.encoding = newres_.apparent_encoding
                newtext = newres_.text
                newtextx = etree.HTML(newtext)
                producturls = self.newInProductUrl(newtextx)
                print(burl, len(producturls))
                alllis = alllis + producturls

                allpagesx = newtextx.xpath('//div[@class="pagination"]/a/text()')
                if len(allpagesx) > 1:
                    allpage = int(allpagesx[-2]) + 1
                else:
                    allpage = 2
                for p in range(2, allpage):
                    # header = self.getHeader()
                    params = {
                        'p': str(p)
                    }
                    newres_ = self.getMet(burl, params)
                    newres_.encoding = newres_.apparent_encoding
                    newtext = newres_.text
                    newtextx = etree.HTML(newtext)
                    producturls = self.newInProductUrl(newtextx)
                    print(newres_.url, len(producturls))
                    if not producturls:
                        break
                    else:
                        alllis = alllis + producturls
            return alllis
        except Exception as e:
            print(traceback.print_exc())
            return -1

    #swimweaer 8 泳装
    def swimEntry(self):
        burls = []
        homeresx = self.homeEntry()
        newStartUrls = homeresx.xpath('/html/body/div[3]/div/div[1]/ul/li[8]/div/ul//a/@href')
        for n in newStartUrls[1:]:
            burl = self.domain + n
            burls.append(burl)
        print(burls)
        alllis = []
        try:
            for burl in burls:
                # header = self.getHeader()
                newres_ = self.getMet(burl)
                newres_.encoding = newres_.apparent_encoding
                newtext = newres_.text
                newtextx = etree.HTML(newtext)
                producturls = self.newInProductUrl(newtextx)
                print(burl, len(producturls))
                alllis = alllis + producturls

                allpagesx = newtextx.xpath('//div[@class="pagination"]/a/text()')
                if len(allpagesx) > 1:
                    allpage = int(allpagesx[-2]) + 1
                else:
                    allpage = 2
                for p in range(2, allpage):
                    params = {
                        'p': str(p)
                    }
                    newres_ = self.getMet(burl, params)
                    newres_.encoding = newres_.apparent_encoding
                    newtext = newres_.text
                    newtextx = etree.HTML(newtext)
                    producturls = self.newInProductUrl(newtextx)
                    print(newres_.url, len(producturls))
                    if not producturls:
                        break
                    else:
                        alllis = alllis + producturls
            return alllis
        except Exception as e:
            print(traceback.print_exc())
            return -1

    #buttoms 9 女式下装
    def buttomsEntry(self):
        burls = []
        homeresx = self.homeEntry()
        newStartUrls = homeresx.xpath('/html/body/div[3]/div/div[1]/ul/li[9]/div/ul//a/@href')
        for n in newStartUrls[1:]:
            burl = self.domain + n
            burls.append(burl)
        print(burls)
        alllis = []
        try:
            for burl in burls:
                # header = self.getHeader()
                newres_ = self.getMet(burl)
                newres_.encoding = newres_.apparent_encoding
                newtext = newres_.text
                newtextx = etree.HTML(newtext)
                producturls = self.newInProductUrl(newtextx)
                print(burl, len(producturls))
                alllis = alllis + producturls

                allpagesx = newtextx.xpath('//div[@class="pagination"]/a/text()')
                if len(allpagesx) > 1:
                    allpage = int(allpagesx[-2]) + 1
                else:
                    allpage = 2
                for p in range(2, allpage):
                    # header = self.getHeader()
                    params = {
                        'p': str(p)
                    }
                    newres_ = self.getMet(burl, params)
                    newres_.encoding = newres_.apparent_encoding
                    newtext = newres_.text
                    newtextx = etree.HTML(newtext)
                    producturls = self.newInProductUrl(newtextx)
                    print(newres_.url, len(producturls))
                    if not producturls:
                        break
                    else:
                        alllis = alllis + producturls
            return alllis
        except Exception as e:
            print(traceback.print_exc())
            return -1

    #accessories 11 饰品
    def accessoriesEntry(self):
        burls = []
        homeresx = self.homeEntry()
        newStartUrls = homeresx.xpath('/html/body/div[3]/div/div[1]/ul/li[11]/div/ul//a/@href')
        for n in newStartUrls[1:]:
            burl = self.domain + n
            burls.append(burl)
        print(burls)
        alllis = []
        try:
            for burl in burls:
                # header = self.getHeader()
                newres_ = self.getMet(burl)
                newres_.encoding = newres_.apparent_encoding
                newtext = newres_.text
                newtextx = etree.HTML(newtext)
                producturls = self.newInProductUrl(newtextx)
                print(burl, len(producturls))
                alllis = alllis + producturls

                allpagesx = newtextx.xpath('//div[@class="pagination"]/a/text()')
                if len(allpagesx) > 1:
                    allpage = int(allpagesx[-2]) + 1
                else:
                    allpage = 2
                for p in range(2, allpage):
                    # header = self.getHeader()
                    params = {
                        'p': str(p)
                    }
                    newres_ = self.getMet(burl, params)
                    newres_.encoding = newres_.apparent_encoding
                    newtext = newres_.text
                    newtextx = etree.HTML(newtext)
                    producturls = self.newInProductUrl(newtextx)
                    print(newres_.url, len(producturls))
                    if not producturls:
                        break
                    else:
                        alllis = alllis + producturls
            return alllis
        except Exception as e:
            print(traceback.print_exc())
            return -1

    #outerweaer 12 男士
    def menEntry(self):
        burls = []
        homeresx = self.homeEntry()
        newStartUrls = homeresx.xpath('/html/body/div[3]/div/div[1]/ul/li[12]/div/ul//a/@href')
        for n in newStartUrls[1:]:
            burl = self.domain + n
            burls.append(burl)
        print(burls)
        alllis = []
        try:
            for burl in burls:
                # header = self.getHeader()
                newres_ = self.getMet(burl)
                newres_.encoding = newres_.apparent_encoding
                newtext = newres_.text
                newtextx = etree.HTML(newtext)
                producturls = self.newInProductUrl(newtextx)
                print(burl, len(producturls))
                alllis = alllis + producturls

                allpagesx = newtextx.xpath('//div[@class="pagination"]/a/text()')
                if len(allpagesx) > 1:
                    allpage = int(allpagesx[-2]) + 1
                else:
                    allpage = 2
                for p in range(2, allpage):
                    # header = self.getHeader()
                    params = {
                        'p': str(p)
                    }
                    newres_ = self.getMet(burl, params)
                    newres_.encoding = newres_.apparent_encoding
                    newtext = newres_.text
                    newtextx = etree.HTML(newtext)
                    producturls = self.newInProductUrl(newtextx)
                    print(newres_.url, len(producturls))
                    if not producturls:
                        break
                    else:
                        alllis = alllis + producturls
            return alllis
        except Exception as e:
            print(traceback.print_exc())
            return -1

    def newExtractField(self,url):
        try:
            # headers = self.getHeader()
            ex_res_ = self.getMet(url)
            ex_res_.encoding = ex_res_.apparent_encoding
            ex_re = ex_res_.text
            # print(ex_res)
            ex_res = etree.HTML(ex_re)

            pattern = re.compile(r'data-mid="(.*?)"', re.S)
            backGroundUrls = pattern.findall(ex_re)

            titlex = ex_res.xpath('//form[@id="details-form"]/h1[@class="product-title trans-ignore"]/text()')
            sale_pricex = ex_res.xpath(
                '//form[@id="details-form"]/div[@class="product-price"]/span[@class="sale-price lang-price"]/text()')
            mark_pricex = ex_res.xpath(
                '//form[@id="details-form"]/div[@class="product-price"]/span[@class="market-price lang-price hidden"]/text()')

            color_listsx = ex_res.xpath('//ul[@class="color__list fix"]/li/@data-value')
            size_listx = ex_res.xpath('//ul[@class="size__list fix"]/li/text()')

            descripex = ex_res.xpath('//div[@class="detail-item__content"]/table[@class="trans-ignore"]/tr')

            size_chartx = ex_res.xpath('//div[@class="detail-item__content size-info-body"]/div/img/@src')

            shipe_returnx = ex_res.xpath('//div[@class="detail-item__content"]/p')
            # print(sale_pricex,mark_pricex)
            print(size_chartx)
            print(size_listx)
            print(descripex)
            print(color_listsx)

        except Exception as e:
            print(traceback.print_exc())
            return -1

if __name__ == '__main__':
    b = Berry()
    header = b.getHeader()
    newres_1 = b.newInEntry()
    print(newres_1)
    b.newExtractField(newres_1[0])



