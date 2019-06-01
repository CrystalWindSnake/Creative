#%%
import numpy as np
import pandas as pd
from pandas import DataFrame
from retrying import retry

import random
import pickle



class Player(object):
  
  def __init__(self, name):
    self.name=name

#%%
class CpuPlayer(Player):
  taken_choice=[1,2,3]

  def __init__(self,name='cpu',learning_mode=True, learning_rate=0.1,searching_rate=0.9,estimated_rate=0.8,max_num=50):
    super(CpuPlayer,self).__init__(name)

    self.learning_rate=learning_rate
    self.searching_rate=searching_rate
    self.estimated_rate=estimated_rate
    self.learning_mode=learning_mode
    self.max_num=max_num
    self._bulid_table()

  def _bulid_table(self):
    self.table=DataFrame(
      data=np.zeros((self.max_num,3)),
      columns=CpuPlayer.taken_choice,
      index=range(1,self.max_num+1)
    )

  def get_taken_num(self, current_num):
    row_value=self.table.loc[current_num,:]

    if self.learning_mode and (row_value.all()==0 or np.random.uniform()>self.searching_rate):
      selected=np.random.choice(CpuPlayer.taken_choice)
    else:
      index=row_value.values.argmax()
      selected=CpuPlayer.taken_choice[index]
    return selected

  def learning(self, current,taken_num,state):
    '''
    state: 1表示赢了，0表示输了,None表示未分胜负
    '''

    reward=self._get_reward(state)

    # 找出选择后的3个可能状态
    next_range_value = self._get_next_range_value(current,taken_num, state)

    em_value=reward+self.estimated_rate * next_range_value
    
    # print(current,taken_num)
    select_value=self.table.loc[current,taken_num]

    # 更新table
    self.table.loc[current,taken_num]+=self.learning_rate*(em_value-select_value)

  def _get_reward(self, state):
    reward=0
    if state==1:
      reward=10 # 因为赢了，给他大奖励
    elif state==0:
      reward=-10 # 因为赢了，给他大惩罚
    return reward

  def _get_next_range_value(self, current,taken_num, state):

    # 如果已经分出胜负，则无需计算状态转移的估计值
    if state is not None:
      return 0

    # 计算当前选择下的可能局面的价值
    end=current-taken_num-1
    start=end-2
    range_df=self.table.loc[start:end,:].copy()

    range_df['all_less']=range_df.apply(lambda x:(x<0).all(),axis=1)
    range_df['all_zero']=range_df.apply(lambda x:(x==0).all(),axis=1)

    # 假如3行中有任意一行全是负数，意味着本次选择有可能会输
    if range_df['all_less'].any():
      return -2
    
    if range_df['all_zero'].any():
      return 0
    
    return range_df.iloc[:,:3].max().max()

  def save_model(self,filename='cpu_play.m'):
    with open(filename,'wb') as f:
      pickle.dump(self,f)
      # json.dumps()
      res=f.name

    return res

  @staticmethod
  def load_from_file(filename='cpu_play.m'):
    with open(filename,'rb') as f:
      return pickle.load(f)

#%%
class Referee(object):
  
  def __init__(self):
    pass

  def ready(self, start_num):
    self.current_num=start_num

  def is_end_game(self):
    return self.current_num<=0

  def get_state(self,taken_num):
    '''
    state: 1表示赢了，0表示输了,None表示未分胜负
    '''
    if self.current_num-taken_num<=0:
      return 0
    
    if self.current_num-taken_num==1:
      return 1
    
    return None
      

  def take_away(self, taken_num):
    self.current_num-=taken_num


class UserPlayer(Player):
  
  def __init__(self,name='user'):
    super(UserPlayer,self).__init__(name)

  @retry
  def get_taken_num(self, current_num):
    ipt=input(f'当前剩余{current_num}个石子,输入你要拿取的数量(1-3):')

    try:
      num=int(ipt)
    except ValueError as ex :
      print('哥，输入数字呀！')
      raise ex

    if num<1 or num>3:
      print('你要输入1到3的数值')
      raise Exception()
    return num





