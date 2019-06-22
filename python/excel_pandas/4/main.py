

#%%
import pandas as pd
import numpy as np
import xlwings as xw

from IPython.display import display
from pyecharts import options as opts
from pyecharts.charts import Bar, Page, Pie, Timeline


# from matplotlib import pyplot as plt
# import seaborn as sns

# plt.style.use({'figure.figsize':(12,8)})
# sns.set_style('darkgrid',{'font.sans-serif':['simhei','Arial']})

#%% 
g_sp_contents=['综合课程','英/生','数/物']

#%%
def display_apart(df):
    display(pd.concat([df.head(3),df.tail(3)]))


def get_df(wb):
    wrk=wb.sheets['data']
    arr=wrk.range('a3').current_region.options(np.array).value
    header=arr[2] # 取出第3行做字段
    values=arr[3:] # 取出第4行以后的做为值
    df=pd.DataFrame(values,columns=header)
    df=df.replace(['/','nan'],np.nan) # 把无用的值用 nan替代

    return df

def reset_header(df):
    cols=df.columns.tolist()
    cols[:3]=['day','apm','num']
    df.columns=cols
    df['num']=df['num'].astype('float').astype('int')
    return df

def fillna(df):
    cols=['day','apm']
    df[cols]=df[cols].fillna(method='ffill')
    return df

def stack(df):
    df=df.set_index(['day','apm','num'])
    df=df.stack()
    df=df.reset_index(-1)
    return df

def split_content(df):
    df.columns=['tmp','name'] # 设置2列名
    # 获取 级别 和 班别
    df['grade']=df['tmp'].apply(lambda x: x[0])
    df['class']=df['tmp'].apply(lambda x: x[1])
    # 科目 和 教师
    df['sj']=df['name'].apply(get_sj)
    df['teach']=df['name'].apply(get_teach)

    df=df.drop(['tmp','name'],axis=1)
    df=df.reset_index()
    return df

def get_sj(content):
    if content in g_sp_contents:
        return content
    return content[:2]

def get_teach(content):
    if content in g_sp_contents or len(content)==2:
        return np.nan
    return content[2:]

#%%
wb=xw.books[0]
df=get_df(wb)
df=reset_header(df)
df=fillna(df)
df=stack(df)
df=split_content(df)

#%%
def create_pie(data,title) -> Pie:
    c = (
        Pie()
        .add("", data)
        .set_global_opts(title_opts=opts.TitleOpts(title=title))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{d}%"))
    )
    return c

def create_grade_pie(grade_values) -> Timeline:
    tl = Timeline()
    sort_keys='一二三四五六七八'
    grade_values=sorted(grade_values.groupby('grade'),key=lambda x: sort_keys.index(x[0]))
    for g,v in grade_values:
        data=[tuple(n) for n in v.iloc[:,1:].values]
        pie =create_pie(data,f'{g}年级科目占比')
        tl.add(pie, f'{g}年级')
    return tl


#%% 语数英合并
cond='语文 英语 数学'.split()
df['sj_class']=df['sj'].apply(lambda x: '语数英' if x in cond else '其他')


#%% 整体 科目占比
res=(
    df.groupby(['sj_class'],sort=True)
        .size()
        .reset_index()
)
res.columns.values[-1]='value'
data=[tuple(n) for n in res.values]
create_pie(data,'整体科目占比').render(r'F:\写作\开发\python\src\Creative\python\excel_pandas\4\test.html')

#%% 班级 科目 占比
res=(
    df.groupby(['grade','sj_class'],sort=True)
        .size()
        .reset_index()
)
res.columns.values[-1]='value'
create_grade_pie(res).render(r'F:\写作\开发\python\src\Creative\python\excel_pandas\4\test.html')

#%% 
res=(
    df.groupby(['teach'],sort=True)
        .size()
        .reset_index()
)
res.columns.values[-1]='value'
res.sort_values('value',ascending=False)

# pd.DataFrame.sort_values(ascending=)

#%%
