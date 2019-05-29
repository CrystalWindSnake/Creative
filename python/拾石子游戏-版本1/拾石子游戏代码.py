
#%%
import random
from retrying import retry

#%%
# 获取开局的值
def get_start_num(start,end):
  return random.randint(start,end)

# 电脑要拿走的数量
def cpu_number(current_num):
  sel=random.randint(1,min(3,current_num))
  return sel

@retry
# 你要拿走的数量
def user_number(current_num):
  inp=input('输入你要拿走的数量(1-3):')
  try:
    num=int(inp)
  except ValueError as ex :
    print('哥，输入数字呀！')
    raise ex

  if num<1 or num>3:
    print('你要输入1到3的数值')
    raise Exception()
  return num

# 判断当前局面是否应该结束
def judge(rule,current_num,selected):
  # 判断是否结束
  def is_end(current_num,selected):
    return current_num-selected<=0

  if is_end(current_num,selected):
    print(f'游戏结束，最后由{rule}把剩余的{num}给拿走了')
  else:
    current_num-=selected
    print(f'{rule}拿走了{selected}，当前剩余:{current_num}')
    return current_num

  return None


#%%
if __name__ == "__main__":
  num=get_start_num(30,50)
  print(f'开局：初始值是{num}')

  while 1:
    cpu_sel=cpu_number(num)

    num=judge('cpu',num,cpu_sel)
    if num is None:
      break

    user_sel=user_number(num)

    num=judge('user',num,user_sel)
    if num is None:
      break



#%%


#%%
