#%%
import requests
from bs4 import BeautifulSoup
import collections as clt

Record=clt.namedtuple('Record','num,event_des,value')
#%%
# 获取网页内容，并返回一个BeautifulSoup
def req_to_bfs():
  pass
  headers={
    'Referer':'http://top.baidu.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
  }
  rp=requests.get('http://top.baidu.com/buzz?',params={'b':341},headers=headers)
  rp.encoding='gbk'

  return BeautifulSoup(rp.text)

# 传入一个BeautifulSoup对象，获取一系列record
def bfs_to_records(bfs):
  mb=bfs.find('div',attrs={'class':'mainBody'})
  tbs=mb.find('table')
  rows=tbs('tr')

  for r in rows[1:]:
    num=get_value_from_td(r('td')[0])
    num=int(num)

    des=get_value_from_td(r('td')[1])
    value=get_value_from_td(r('td')[3])
    yield Record(num,des,value)

# 只是一个方便提取文本内容的小方法
def get_value_from_td(td):
  return list(td.stripped_strings)[0]

#%%
if __name__ == "__main__":
  bs=req_to_bfs()
  print(list(bfs_to_records(bs)))