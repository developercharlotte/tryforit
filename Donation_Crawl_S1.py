# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 23:22:16 2018

@author: Leo
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import pandas as pd

def getHTMLText(url, data):
       try:
              r = requests.post(url, data=data)
              r.raise_for_status()
              r.encoding = r.apparent_encoding
              return r
       except:
              return ""

def getProCode(url, page):
       dic = {}
       dic['step'] = 'get_campaigns_by_campaign_type'
       dic['campaign_type'] = 'successful'
       dic['lang'] = 'en'
       dic['exclud_camp'] = '0'
       MaxPage = page
       start_time = time.time()
       for i in range(1, MaxPage+1):
              dic['page'] = i
              html = getHTMLText(url, dic).text
              try:
                     if html == "":
                            continue
                     else:
                            try:
                                   soup = BeautifulSoup(html, 'html.parser')
                            except:
                                   html = getHTMLText(url, dic).content
                                   soup = BeautifulSoup(html, 'html.parser')
                            img = soup.find_all('img')
                            pat0 = re.compile(r'/\d{4}/\d{2}/')
                            pat1 = re.compile(r'\d*/img')
                            pat2 = re.compile(r'^<.*><img')
                            for j in img:
                                   src = j.attrs['src']
                                   loc = img.index(j)
                                   
                                   date = pat0.findall(src)[0][1:-1]
                                   df.at[(i-1)*12+loc,'Date'] = date
                                   
                                   code = pat1.findall(src)[0][:-4]
                                   df.at[(i-1)*12+loc,'Project_Code'] = code
                                   ''' 找到img的父节点并提取网站 '''
                                   parent = str(j.parent)
                                   web = pat2.findall(parent)[0].split('"')[1]
                                   df.at[(i-1)*12+loc,'Website'] = web
                            time.sleep(0.5)
                            end_time = time.time()
                            remain_time = (end_time-start_time)/i*(MaxPage-i)
                            print("\r{:>6.2f}% Done, Time Remained: {:04}:{:02}:{:02}".format(
                                          (i*100/MaxPage), int(remain_time//3600), 
                                          int(remain_time//60%60), int(remain_time%60)),
                                   end="")
              except:
                     continue
                            
df = pd.DataFrame({'Project_Code':'', 'Website':'', 'Date':''}, index=range(0,500))
url_suc = 'https://gogetfunding.com/wp-content/themes/ggf/campaigns.php'
getProCode(url_suc, 20)

ret_path = r'C:\Users\charl\Desktop\ProCode.csv'
df.to_csv(ret_path, encoding='utf-8', index=False)