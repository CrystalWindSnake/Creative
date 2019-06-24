

#%%
import pandas as pd
import numpy as np

from pyecharts import options as opts
from pyecharts.charts import Bar, Page, Pie, Timeline


#%%
def get_df():
    return pd.read_csv('data.csv',encoding='utf8')

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


def create_teach_bar(*dfs) -> Bar:
    def create_one_bar(df,day=None):
        df=df.sort_values(['rank','teach'])
        am_values=df.query('apm=="上午"')
        pm_values=df.query('apm=="下午"')
        names=am_values['teach'].values.tolist()

        title= f'({day})教师课时数' if day else '教师课时数'

        b = (
            Bar()
            .add_xaxis(names)
            .add_yaxis('上午', am_values['value'].values.tolist(), stack="stack1")
            .add_yaxis('下午',pm_values['value'].values.tolist(), stack="stack1")
            # .reversal_axis()
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
                title_opts=opts.TitleOpts(title=title),
                datazoom_opts=opts.DataZoomOpts(type_='slider',range_start=0,range_end=10),
            )
        )
        return b

    if len(dfs)==1:
        return create_one_bar(dfs[0])

    page=Page()
    
    for df in dfs:
        day=df['day'].iloc[0]
        b=create_one_bar(df,day)
        page.add(b)
    return page

#%%
df=get_df()
df

#%% 语数英合并
cond='语文 英语 数学'.split()
df['sj_class']=df['sj'].apply(
    lambda x: '语数英' if x in cond else '其他')

df.head(5).append(df.tail(5))

#%% 整体 科目占比
res=(
    df.groupby(['sj_class'])
        .size()
        .reset_index()
)
res.columns.values[-1]='value'
data=[tuple(n) for n in res.values]
create_pie(data,'整体科目占比').render(r'整体科目占比.html')


#%% 班级 科目 占比
res=(
    df.groupby(['grade','sj_class'],sort=True)
        .size()
        .reset_index()
)
res.columns.values[-1]='value'
create_grade_pie(res).render(r'级别科目占比.html')

#%% apm 教师课时
res=(
    df.groupby(['teach','apm'],sort=True)
        .size()
        .reset_index()
)
res.columns.values[-1]='value'

res=(
    res.set_index(['teach','apm'])
        .unstack()
        .stack(dropna=False)
        .reset_index()
)
res

#%%
# 为了补齐缺少上午或下午的行
res=(
    res.set_index(['teach','apm'])
        .unstack()
        .stack(dropna=False)
        .reset_index()
)

# 统计课时数，然后排名。
res['total']=res.groupby('teach')['value'].transform('sum')
res['rank']=res['total'].rank(ascending=False)

# 为了方便看数据
res=res.sort_values(['rank','teach'])
# 输出图表
create_teach_bar(res).render(r'教师上下午课时.html')


#%% apm 每天 教师课时
res=(
    df.groupby(['teach','apm','day'],sort=True)
        .size()
        .reset_index()
)
res.columns.values[-1]='value'
# 为了补齐缺少上午或下午的行
res=(
    res.set_index(['teach','apm','day'])
        .unstack(['apm','day'])
        .stack(['apm','day'],dropna=False)
        .reset_index()
)

# 统计课时数，然后排名。
res['total']=res.groupby(['teach','day'])['value'].transform('sum')
res['rank']=res['total'].rank(ascending=False)

# 为了方便看数据
res=res.sort_values(['day','rank','teach'])
# 输出图表
day_dict={n:i for i,n in enumerate('一二三四五')}
res=sorted(res.groupby('day'),key=lambda x: day_dict[x[0][-1]])
res=[g[1] for g in res]
create_teach_bar(*res).render(r'教师每天课时.html')

#%%






#%%
res[0]
#%%
