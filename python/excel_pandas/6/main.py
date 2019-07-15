#%%
import pandas as pd

g_pName='开单部门'
g_sku_code='货品编码'
g_sku_name='货品名称'
g_num='数量'
g_price='价税合计'
g_barcode='条型码'

g_titles=[g_pName,g_sku_code,
    g_sku_name,g_num,
    g_price,g_barcode]

g_agg_funcs={
    g_sku_name:'first',
    g_num:'sum',
    g_price:'sum',
    g_barcode:'first',
    g_sku_code:'first',
    '单价':'mean'
}

#%%
def get_df(header_row=3):
    df=pd.read_excel('fake_data.xlsx',header=None)
    header_idx=header_row-1
    # 获取标题行给 df
    header=df.iloc[header_idx,:]
    df.columns=header
    # 获取需要的行和列
    # df = df[g_titles]
    df = df.iloc[header_idx+1:,:]
    df = df.dropna(subset=[g_pName])
    df['单价']=df['单价'].astype('float')
    return df

#%%

#%%
df = get_df()

#%%
# 按 销售员和货品分组统计
cols=[g_pName,g_sku_code]
res=df.groupby(cols).agg(g_agg_funcs)
res

#%%
# 每个组结果输出每个sheet
with pd.ExcelWriter('result.xlsx') as exl:
    for idx in set(res.index.get_level_values(0)):
        res.loc[idx,:].to_excel(exl,
            sheet_name=f'{idx}销售表',
            index=False,
            startrow=1)

    exl.save()

#%%
# 按货品汇总
res=df.groupby(g_sku_code).agg(g_agg_funcs)

with pd.ExcelWriter('result.xlsx',engine='openpyxl',mode='a') as exl:
    res.to_excel(exl,
            sheet_name='所有货品销售表',
            index=False,
            startrow=1)
    exl.save()
#%%



#%%
