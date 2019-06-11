#%%
import os
import pathlib
import shutil



#%% 
def get_file_names(folder):
    '''
    返回的文件名是不包含后缀的噢
    '''
    paths=pathlib.Path(folder).glob('*.mp4')
    return (p.stem for p in paths)

def get_new_name(file_name):
    name,num=file_name.split('-')
    return f'{name}({num})'

def rename(folder,org_name,new_name):
    folder=pathlib.Path(folder)
    org_path=folder.joinpath(f'{org_name}.mp4')
    new_path=folder.joinpath(f'{new_name}.mp4')

    org_path.rename(new_path)


#%% 
# 准备数据
def data_ready():
    set_chdir()
    create_samples()

def create_samples():
    folder='files'
    shutil.rmtree(folder)
    os.makedirs(folder,exist_ok=True)
    for i in range(1,16):
        with open(f'{folder}/剧名-{i}.mp4','w') as f:
            pass

def set_chdir():
    try:
        path=pathlib.Path(__file__)
        os.chdir(path.parent)
    except :
        pass


data_ready()

def display_message(folder,modify_msgs):
    print(f'本次操作文件夹:{pathlib.Path(folder).resolve()}')
    print('以下为变动明显：')
    print('='*20)
    for org,new in modify_msgs:
        print(f'{org} -> {new}')

    print('='*20)

if __name__ == "__main__":
    folder='files'
    org_news=[
        (org,get_new_name(org))
        for org in get_file_names(folder)
    ]

    display_message(folder,org_news)
    ipt=input('输入 Y/y 将执行修改:')
    if ipt.upper()!='Y':
        print('已取消操作')
        exit()

    for org,new in org_news:
        rename(folder,org,new)

    print('完成修改！')

#%%
