from random import randint
import pathlib
import os

from wordcloud import WordCloud
import jieba
import imageio

# 参考资料
# https://blog.csdn.net/u010152318/article/details/80242460
# https://blog.csdn.net/guduruyu/article/details/77540445

class RandomColorFunc(object):

    def __init__(self):
        self.color_dict={}

    def color_func(self,word=None, font_size=None, position=None,  orientation=None, font_path=None, random_state=None):
        '''
        控制每个词的显示颜色
        '''

        # 记录每个词的hsl值，然后每次把s(饱和度)增加10
        if word in self.color_dict:
            self.color_dict[word][1]+=10
            if self.color_dict[word][1]>100:
                self.color_dict[word][1]=0
            return "hsl({}, {}%, {}%)".format(*self.color_dict[word])

        h  = randint(120,250)
        s = 0
        l = int(100.0 * float(randint(60, 120)) / 255.0)
        self.color_dict[word]=[h,s,l]
        return "hsl({}, {}%, {}%)".format(h, s, l)


def get_content(file_path):
    '''
    获取内容并分词
    '''
    with open(file_path,encoding='utf8') as f:
        content=''.join(f.readlines()) 

    cut=jieba.cut(content)
    content=' '.join(cut)
    return content

def create_cloud_imgs(content,pict_dir,pict_count=10):
    '''
    创建词云图片
    '''
    os.makedirs(pict_dir,exist_ok=True)
    font = r'FZSTK.TTF' # 这个是中文字体。如果内容是中文必需指定。

    color_func=RandomColorFunc()

    for i in range(1,pict_count+1):
        wc=WordCloud(font_path=font,
                    background_color='white',
                    stopwords=['可以','即可'],
                    color_func =color_func.color_func,
                    random_state=40).generate(content)

        wc.to_file(f'{pict_dir}/{i}.png')
        print(f'成功保存图片{i}',end='\r')

    print(f'生成词云图片完毕({pict_count}张)')


def create_gif(folder,gif_name='res.gif'):
    '''
    创建动态图
    '''
    dir=pathlib.Path(folder)
    files=dir.glob('*.png')
    files=sorted(files,key=lambda x: int(x.stem))
    files=[
        imageio.imread(n)
        for n in files
    ]

    imageio.mimsave(gif_name,files,'GIF',duration=0.5)
    print(f'生成gif图片:{pathlib.Path(gif_name).resolve()}')



if __name__ == "__main__":
    os.chdir(pathlib.Path(__file__).parent)

    pict_path='picts'

    print('获取分词')
    content=get_content('content.txt')

    print('开始生成词云图片')
    create_cloud_imgs(content,pict_path)

    print('生成gif')
    create_gif(pict_path)


