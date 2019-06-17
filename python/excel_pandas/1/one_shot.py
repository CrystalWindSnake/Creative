
#%%
import xlwings as xw
import pandas as pd

wb=xw.books['成绩单.xlsx']
wrk=wb.sheets['Sheet1']

df=wrk.range('a1').current_region.options(pd.DataFrame).value
# 透视
pv_df=pd.pivot_table(df,
        index='班级',
        margins=True,
        margins_name='科目总平均')
# 调整结果
cols='语文,数学,英语,物理,历史,地理,政治,生物,总分'.split(',')
pv_df=pv_df[cols]
pv_df.reset_index(inplace=True)
# 输出
wrk.range('O11').value=pv_df.columns.tolist()
wrk.range('O12').value=pv_df.values



#%%
df

#%%
