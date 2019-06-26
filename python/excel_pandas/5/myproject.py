
import pandas as pd
import numpy as np
import xlwings as xw
from pathlib import Path

path=r"Financial Sample.xlsx"
full_path=str(Path(__file__).parent.joinpath(path))

def where_df(df,where_exp=''):
    where_exp=where_exp.strip()
    if where_exp is None or len(where_exp)==0:
        return df
    return df.query(where_exp)

def group_df(df,groups,values,date_freq='M',agg_func='mean'):
    date_gp=pd.Grouper(key='Date',freq=date_freq)
    res=(
        df
        .groupby([date_gp,*groups])
        [values]
        .agg(agg_func)
        .reset_index()
    )
    return res

@xw.func
def get_result_vba(where,groups,values,date_freq='M',agg_func='mean'):
    df=pd.read_excel(full_path,sheet_name='data')
    
    groups=groups.split(',')
    values=values.split(',')

    res=where_df(df,where)
    res=group_df(res,groups,values,date_freq,agg_func)
    # 整理输出的结果。
    # 为了把表头和结果一起输出，因此下面把表头的和值，2个数组合并
    title=res.columns.values.reshape(1,-1)
    if len(res)==0:
        res_values=np.full_like(title,fill_value=np.nan)
    else:
        res_values=res.values

    res=np.concatenate((title,res_values),axis=0)
    return res
