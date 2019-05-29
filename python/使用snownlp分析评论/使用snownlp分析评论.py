#%% 导入
import snownlp as slp
import collections as clt

#1
Comment=clt.namedtuple('Comment','content,result')

#%% 方法定义 
def get_contents(file_path):
  with open(file_path,'r',encoding='utf8') as f:
    return [n.strip() for n in f.readlines()]

def analyse_to_comment(content):
  #2
  s=slp.SnowNLP(content)
  #3
  return Comment(display_long(content),pst_to_result(s.sentiments))
    
def display_long(content):
  if len(content)>10:
    return f'{content[0:5]}……{content[-5:]}'
  return content

#4
def pst_to_result(positive):
  if positive>0.75:
    return '好评'
  return '差评'


#%% 运行
if __name__ == "__main__":
  file=r'taobao评论.txt'
  cms=(
    analyse_to_comment(c) 
    for c in get_contents(file)
  )
  for c in cms:
    print(c)