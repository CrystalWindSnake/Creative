from models import CpuPlayer,Referee,UserPlayer
import itertools as itl
from retrying import retry


def training_cpu(game_times=100):
  print(f'开始训练……数量{game_times}轮')
  cpu=CpuPlayer()
  refer=Referee()

  for r in range(game_times):
    refer.ready(50)

    for _ in itl.cycle([1,2]):
      taken=cpu.get_taken_num(refer.current_num)
      state= refer.get_state(taken)
      cpu.learning(refer.current_num,taken,state)
      refer.take_away(taken)

      if refer.is_end_game():
        break

    if r%5==0:
      print(f'第{r}轮训练完成')
    

  model_path=cpu.save_model()
  print(f'所有训练完成，model保存到文件:{model_path}')


def play_game(start_num=49):
  pass
  try:
    cpu=CpuPlayer.load_from_file()
    cpu.learning_mode=False
  except FileNotFoundError:
    print(f'找不到model文件,请先训练电脑')
    return

  user=UserPlayer()
  player_iter=iter(itl.cycle([cpu,user]))

  refer=Referee()
  refer.ready(start_num)

  print(f'开始游戏，开始数量:{refer.current_num}')

  for player in player_iter:
    print('='*10)
    print(f'本轮由[{player.name}]行动')
    taken=player.get_taken_num(refer.current_num)
    refer.take_away(taken)

    print(f'[{player.name}]拿走{taken}个石子，当前剩余数:{refer.current_num}')

    if refer.is_end_game():
      print('!'*15)
      print(f'[{player.name}]输了，[{next(player_iter).name}]赢了')
      print('!'*15)
      break

def display_cpu_table():
  cpu=CpuPlayer.load_from_file()
  print(cpu.table)


@retry
def menu():
  ipt=input('1：训练电脑玩家\n2：与电脑对战\n')

  try:
    num=int(ipt)
  except ValueError as ex :
    print('哥，输入数字呀！')
    raise ex

  if num<1 or num>2:
    print('你要输入1到2的数值')
    raise Exception()
  
  funcs={
    1:[training_cpu,{}],
    2:[play_game,{'start_num':11}]
  } 

  func_list=funcs[num]
  func=func_list[0]
  args=func_list[1]
  func(**args)
  raise Exception()

if __name__ == "__main__":
  menu()
  # display_cpu_table()
