import csv
import random
import time

from bs4 import BeautifulSoup
import requests
from lxml import etree
import re



main_url = "http://www.appchina.com/category/30/{}_1_1_3_0_0_0.html"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}


def get_ip():
    proxy_url = 'http://http.tiqu.letecs.com/getip3?num=20&type=2&pro=&city=0&yys=0&port=1&pack=214142&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=&gm=4'
    json_data = requests.get(url=proxy_url,headers=headers).json()
    json_list = json_data['data']
    proxy_list = [] #代理池,每次请求，可以随机从代理池中选择一个代理来用
    for dic in json_list:
        ip = dic['ip']
        port = dic['port']
        n_dic = {
            'https':ip+':'+str(port) # {'https':'111.1.1.1:1234'}
        }
        proxy_list.append(n_dic)
    for ip in proxy_list:
        yield ip

def spider():
    with open('app_link.csv', 'a', encoding='utf-8', newline='') as f:
        finaname = ['app名称', '下载网址']
        csv_data = csv.DictWriter(f, fieldnames=finaname)
        csv_data.writeheader()
        while 1:
            try:
                proxy_ip = next(gen)
                proxy = {
                    "http":"http://"+proxy_ip,
                    "https":"https://"+proxy_ip,

                }

                for i in range(1, 3295):
                    response = requests.get(url=main_url.format(i), headers=headers,proxies=proxy).text
                    html = etree.HTML(response)
                    li_list = html.xpath('//*[@id="left"]/ul')
                    for li in li_list:
                        li_url = li.xpath('./li/a/@href')
                        for link in li_url:
                            url = "http://www.appchina.com" + link
                            res = requests.get(url, headers=headers,proxies=proxy)
                            if res.status_code ==200:
                                html = etree.HTML(res.text)
                                item = {}
                                item['app名称'] = html.xpath('//*[@id="pagecontainer"]/div[3]/div[1]/div[1]/div/h1/text()')[0]
                                item['下载网址'] = html.xpath('//*[@id="pagecontainer"]/div[3]/div[1]/div[2]/div[1]/div/a/@onclick')[0].split( "'")[1]
                                # rows = [name, app_link]
                                # for row in rows:
                                csv_data.writerow(item)
                                print(item['下载网址'], "下载完毕")
                            else:
                                return


            except Exception as e:
                print(e)


if __name__ == '__main__':
    gen = get_ip()
    spider()





