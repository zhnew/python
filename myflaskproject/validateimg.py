#coding:utf-8
import PIL
import Image, ImageDraw, ImageFont,ImageFilter
from random import randint
from cStringIO import StringIO

CHAR = 'acdefghijkmnpqrstuvwxy012345789' 
PADDING = 30 
FONT = ImageFont.truetype('arial.ttf',24)

def gen():
    im = Image.new('RGB', (90, 40), '#f0ff02')
    draw = ImageDraw.Draw(im)
    w, h = im.size

    S = []
    x_list = []

    while len(S)<4:
        if len(x_list)==0:
            x=8
        else:
            x = x_list[-1]+12+randint(0,5)
        y = randint(0, h - PADDING-5)
        x_list.append(x)
        S.append((x, y, CHAR[randint(0, len(CHAR)-1)]))

    for x, y, c in S:
        draw.text((x, y), c, font=FONT,fill=(255,0,255))

    #加3根干扰线
    for i in range(3):
        x1 = randint(0, (w - PADDING) / 2)
        y1 = randint(0, (h- PADDING / 2))
        x2 = randint(0, w)
        y2 = randint((h - PADDING / 2), h)
        draw.line(((x1, y1), (x2, y2)), fill=0, width=1)

    # 图形扭曲参数
    params = [1 - float(randint(1, 2)) / 100,
              0,
              0,
              0,
              1 - float(randint(1, 10)) / 100,
              float(randint(1, 2)) / 500,
              0.001,
              float(randint(1, 2)) / 500
              ]
    im = im.transform(im.size, Image.PERSPECTIVE, params) # 创建扭曲
    im = im.filter(ImageFilter.EDGE_ENHANCE_MORE) # 滤镜，边界加强

    char = [x[2] for x in S]
    fileio = StringIO()
    im.save(fileio, 'gif')
    return ''.join(char), fileio

if __name__ == '__main__':
    print gen()  
