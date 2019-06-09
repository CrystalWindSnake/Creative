#%%
nums=[1,2,3,4]

# 通过索引访问
for i in range(0,4):
    n=nums[i]
    print(n)

# 直接遍历
for n in nums:
    print(n)


#%%
for n1 in nums:
    for n2 in nums:
        print(n1,n2)



#%%
tor=iter(nums)

while 1:
    try:
        n=next(tor)
        print(n)
    except StopIteration:
        break


#%%
tor=range(1,10)

list(tor)
list(tor)
tor
#%% 生成器推导式
from collections.abc import Iterator

gen=(n for n in nums)

print(isinstance(gen,Iterator))
print(list(gen))
print(list(gen))

#%% 生成器函数
def gen_func():
    i=0
    while 1:
        yield i

isinstance(gen_func(),Iterator)


#%%
class MyNums(object):
    
    def __init__(self):
        self.values=[1,2,3,4]

    def __getitem__(self,index):
        return self.values[index]

mn=MyNums()

for n in mn:
    print(n)

#%%
