#%%
import xlwings as xw
import pandas as pd
import numpy as np

from matplotlib import pyplot as plt
import seaborn as sns

plt.style.use({'figure.figsize':(12,8)})
sns.set_style('darkgrid',{'font.sans-serif':['simhei','Arial']})

def get_wb_wrk(book_name):
    wb=xw.books[book_name]
    wrk=wb.sheets['Sheet1']
    return wb,wrk

def get_df(wrk):
    df=wrk.range('a1').current_region.options(pd.DataFrame).value
    df.reset_index(inplace=True)
    df['班级']=df['班级'].astype('int')
    df['性别']=df['性别'].astype('category')
    return df

#%%
wb,wrk=get_wb_wrk('成绩单.xlsx')
df:pd.DataFrame=get_df(wrk)

#%%
df.describe(include='all')

#%%
sns.catplot(data=df,
    x='性别',
    y='总分',
    kind='box',
    height=7,
    fliersize =10)


#%%
df.query('总分<500 & 性别=="女"').count()

#%%
df.query('性别=="男"')['总分'].mean()

#%%
sns.catplot(data=df,
    x='班级',
    y='总分',
    # hue='班级',
    kind='violin',
    height=15,aspect=1.5)



#%%
df.groupby('班级').agg('std')

#%%
df.groupby('班级').agg('mean').stack().unstack(0)


#%%
tmp_df.reset_index()

#%%
df.describe()

#%%
