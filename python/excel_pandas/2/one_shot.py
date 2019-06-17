
#%%
import xlwings as xw
import pandas as pd
import numpy as np

def get_wb_wrk(book_name):
    wb=xw.books[book_name]
    wrk=wb.sheets['Sheet1']
    return wb,wrk

def get_df(wrk):
    df=wrk.range('a1').current_region.options(pd.DataFrame).value
    df.reset_index(inplace=True)
    df['班级']=df['班级'].astype('int')
    return df

#%%
def set_color(top_range,arg_df,cols_count,color):
    indices=(n for n in arg_df.index)
    for i in indices:
        rng=top_range.offset(i).resize(1,cols_count)
        rng.api.Interior.Color = color


#%%
top3_color=15773696
below_color=255
cols=11

wb,wrk=get_wb_wrk('成绩单.xlsx')
df=get_df(wrk)

# 排名与平均分
df['排名']=df.groupby('班级')['总分'].rank(ascending=False,method='min')
df['班级均分']=df.groupby('班级')['总分'].transform('mean')
# 获得结果
top3_df=df.query('排名<=3')
below_avg=df.query('总分<班级均分')
# 设置颜色
set_color(wrk.range('A2'),top3_df,cols,top3_color)
# set_color(wrk.range('A2'),below_avg,cols,below_color)




