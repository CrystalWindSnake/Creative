#%% 
# 导入与全局设置
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from IPython.display import display

sns.set(style="darkgrid")
plt.style.use({'figure.figsize':(12, 8)})
path=r'data/titanic.csv'


#%% 
import warnings
warnings.filterwarnings("ignore")
def add_person_group(df):
    count_df=df.groupby('ticket')['ticket'].count()
    idx= count_df[count_df>1].index.values
    where=df['ticket'].isin(idx)
    df['person_group']=where
    df['person_group']=df['person_group'].astype('category')
    df['person_group'].cat.categories=['single','group']




#%% 
# 载入数据
df=pd.read_csv(path)

display(df.head(5))

display(df.describe(include='all'))

display(df.isnull().sum())


#%% 
# 简单处理
df['sex']=df['sex'].astype('category')
df.dropna(subset=['age'],inplace=True)
df['age_group']=pd.qcut(df['age'],10)
add_person_group(df)

#%% 
# 性别的生存率情况
sns.factorplot(x='sex',y='survived',data=df,kind='bar',size=7)

#%% 
# 年龄分组的生存率
sns.factorplot(x='age_group',y='survived',data=df,kind='bar',size=10)

#%% 
# 性别+年龄
sns.factorplot(
    x='age_group',
    y='survived',
    data=df,
    kind='bar',
    col='sex',
    size=10)

#%% 
# 查看第一组的小孩子数据
first=df['age_group'].cat.categories[0]
first_df=df[df['age_group']==first]
first_df

#%% 
# 有2个佣人，只救了1个小孩逃离
# 为什么推断是2个佣人？
df[df['ticket']=='113781']


#%%
sns.factorplot(x='person_group',
    y='survived',
    data=df,
    kind='bar',
    # col='sex',
    size=8)




#%%
