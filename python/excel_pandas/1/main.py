
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
    df.drop('姓名',axis=1,inplace=True)
    # df['班级']=df['班级'].astype('int')
    return df

def get_pivot_df(df):
    pv_df=pd.pivot_table(df,
        index='班级',
        margins=True,
        margins_name='科目总平均')
    
    # 最终显示的字段顺序
    cols=df.columns[1:].tolist()
    pop_idx=cols.index('总分')
    cols.append(cols.pop(pop_idx))

    pv_df=pv_df[cols]
    pv_df.reset_index(inplace=True)
    return pv_df

def output(range,df):
    range.value=df.columns.tolist()
    range.offset(1).value=df.values

#%%
wb,wrk=get_wb_wrk('成绩单.xlsx')
df=get_df(wrk)
pv_df=get_pivot_df(df)
output(wrk.range('O11'),pv_df)




#%%
