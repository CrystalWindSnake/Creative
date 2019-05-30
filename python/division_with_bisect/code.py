#%% 导入
import bisect as bs
import collections as clt
Student=clt.namedtuple('Student','name,score')

#%% 数据
score_range=[60,80,90]
comments=['好好学做人吧','勉强可以','很不错','你前途无量']

students=[
  Student('张三',59),
  Student('李四',60),
  Student('王五',79),
  Student('罗七',80),
  Student('吴八',89),
  Student('杜九',90),
  Student('周十',95),
]

#%% 实现部分
# 找出每个人的所属评价的索引
res_indices= (
  bs.bisect(score_range,s.score) 
  for s in students
  )

# 通过索引找出对应的评价数据
res=(
  (s,comments[i])
  for i,s in zip(res_indices,students)
)

print(list(res))



#%%
