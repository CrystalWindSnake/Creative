

#%%
import pandas as pd
from IPython.display import display
import numpy as np
#%%
df=pd.DataFrame({
    'class':['C1','C1','C1','C2','C2','C2'],
    'name': ['A1','A2','A3','A4','A5','A6'],
    'age':[21,22,23,24,25,26],
    'value':[100,200,300,400,500,600]
})

df
#%% groupby
class_group=df.groupby('class')

class_group=df.groupby(df['class'])

for g in class_group:
    display(g)

#%% groupby 传入值
df.groupby([1,1,1,2,2,2])


#%% apply + np.mean
class_group.apply(np.mean)

#%% apply + custom func
def apply_func(arg_df):
    res=arg_df['value']-arg_df['age']
    # print(res)
    return res

class_group.apply(apply_func)

#%% apply + custom func + args
# value 列减去指定值的新列
def apply_func(arg_df,add_value):
    arg_df['value']=arg_df['value']+add_value
    return arg_df

class_group.apply(apply_func,add_value=-10)


#%% agg
class_group.agg(np.mean)

#%% apply + custom func
def agg_func(arg_series):
    # 不要向下面那样尝试访问某列，因为arg_series不是DataFrame。
    # arg_series['value'] 
    return arg_series.mean()

class_group.agg(agg_func)


#%% transform
class_group.transform(np.mean)


#%%
def transform_func(arg):
    return arg

class_group[['value','age']].transform(transform_func)


#%% 组内均值填充
def transform_func(arg_series):
    return arg_series.fillna(arg_series.mean())

res_df=df.copy()
res_df.loc[1:4,'value']=np.nan

res_df['new_value']=(res_df.groupby('class')['value']
        .transform(transform_func))
res_df


#%% 以 value 列为标准，得出每个分组的 top 2的人。
def top_n(arg_df,n,by):
    return (arg_df
        .sort_values(by,ascending=False)
        .iloc[:n,:].copy())

class_group.apply(top_n,n=2,by='value')

#%%
