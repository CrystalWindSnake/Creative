#%%
nums=[1,3,-1,-5,6,-4,10,20]

res=[]
for n in nums:
    if n>0:
        res.append( n )

res

#%% 
nums=[1,3,-1,-5,6,-4,10,20]

res=[
    n 
    for n in nums 
    if n>0
]

res

#%%
def get_nums_from_file(file_path):
    with open(file_path) as f:
        return [int(n.strip()) for n in f.readlines()]

paths=[
    '1.txt',
    '2.txt',
    '3.txt'
]



#%%
res=[
    (n,f)
    for f in paths
    for n in get_nums_from_file(f)
    if n<50
]

res

#%%
res=[
    (n,f)
    for f in paths
    for n in get_nums_from_file(f)
    if n<50
]

res

#%%
def avg(nums):
    return sum(nums)/len(nums)

res=[
    (n,f,avg(get_nums_from_file(f)))
    for f in paths
    for n in get_nums_from_file(f)
    if n < avg(get_nums_from_file(f))
]

res


#%%
res=[]
for f in paths:
    nums=get_nums_from_file(f)
    mean=avg(nums)

    for n in nums:
        if n < mean:
            res.append((n,f,mean))

res

#%%
def get_nums_from_file_mean(path):
    nums=get_nums_from_file(path)
    return nums,avg(nums)

res=[
    (n,f,avg(get_nums_from_file(f)))
    for f in paths
    for  in get_nums_from_file_mean(f)
    if n < avg(get_nums_from_file(f))
]

res

#%%
