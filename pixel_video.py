import argparse
import cv2
import shutil
import os
import sys
import time
from PIL import Image, ImageDraw, ImageFont

ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")

def read_video(video_name):
    vp = cv2.VideoCapture(video_name) #now vp stands for the vedio
    number = 0
    if vp.isOpened():
        print("successful read the video")
        r, frame = vp.read()
        if not os.path.exists('cache_pic'):
            os.mkdir('cache_pic')
        shutil.rmtree('cache_pic')
        os.mkdir('cache_pic')
        os.chdir('cache_pic')
    else:
        print("not such video!!!")
        sys.exit(0) 
    frame_count = int(vp.get(cv2.CAP_PROP_FRAME_COUNT))
    while r:
        number += 1
        print("\r", end="")  #顶天星科技进度条：
        print("Video loading progress: %d/%d"%(number,frame_count),"▋ " * round(30*number/frame_count),"- " * round(30*(frame_count-number)/frame_count),end="")
        sys.stdout.flush()
        cv2.imwrite(str(number) + '.jpg', frame)
        r, frame = vp.read()
    print()
    os.chdir("..")
    return frame_count

def get_char(r,g,b,alpha = 256):

    # 判断 alpha 值
    if alpha == 0:
        return ' '

    # 获取字符集的长度，这里为 70
    length = len(ascii_char)
    
    # 将 RGB 值转为灰度值 gray，灰度值范围为 0-255
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)

    # 灰度值范围为 0-255，而字符集只有 70
    # 需要进行如下处理才能将灰度值映射到指定的字符上
    unit = (256.0 + 1)/length
    
    # 返回灰度值对应的字符
    return ascii_char[int(gray/unit)]

def change_pic(frame_count):
    if frame_count <= 1:
        sys.exit(0) 
    else:
        os.chdir('cache_pic')
    numberr = frame_count
    while frame_count:
        IMG = str(numberr-frame_count+1) + '.jpg'
        WIDTH = 977
        HEIGHT = 110
        OUTPUT = str(numberr-frame_count+1) + '.txt'
        im = Image.open(IMG)
        real_width, real_height = im.size
        rate = real_height/real_width
        WIDTH = round(1.75*HEIGHT/rate)
        im = im.resize((WIDTH,HEIGHT), Image.NEAREST)#HEIGHT will keep at 359
        txt = ""
        for i in range(HEIGHT):
            for j in range(WIDTH):
                txt += get_char(*im.getpixel((j,i)))
            txt += '\n'
        with open(OUTPUT,'w') as f:
            f.write(txt)
        print("\r", end="")  #顶天星科技进度条：
        print("Generate txt file: %d/%d"%((numberr-frame_count+1),numberr),"▋ " * round(30*(numberr-frame_count)/numberr),"- " * round(30*frame_count/numberr),end="")
        frame_count = frame_count - 1
    print()
    os.chdir("..")

def char_to_img(frame_count):
    if not os.path.exists('char_img'):
        os.mkdir('char_img')
    shutil.rmtree('char_img')
    os.mkdir('char_img')
    numberr = frame_count
    while frame_count:
        os.chdir('cache_pic')
        pic = str(frame_count) + '.txt'
        with open(pic,"r") as f:
            data = f.read()
        os.chdir("..")
        os.chdir('char_img')
        im_txt = Image.new("RGB",(2300,1450),(0,0,0))
        dr = ImageDraw.Draw(im_txt)
        font = ImageFont.load_default().font
        x=y=0
        #获取字体的宽高
        font_w,font_h=font.getsize(data[1])
        font_h *= 1.15 #调整后更佳
        #ImageDraw为每个ascii码进行上色
        for i in range(len(data)):
            if(data[i]=='\n'):
                x+=font_h
                y=-font_w
            dr.text([y,x],data[i],(225,225,225))
            y+=font_w
                    #输出
        name = str(frame_count) + '.jpg'
        print("\r", end="")  #顶天星科技进度条：
        print("Convert txt files to images: %d/%d"%((numberr-frame_count+1),numberr),"▋ " * round(30*(numberr-frame_count)/numberr),"- " * round(30*frame_count/numberr),end="")
        im_txt.save(name)
        frame_count = frame_count - 1
        os.chdir("..")
    print()

def charts2video(img_path, video_path, frame_count):
    """将给定目录下的图片转成视频
    Args:
        img_path: 图片路径
        video_path: 输出视频的路径和名称
    Returns: 图片转成的视频
    """
    images = os.listdir(img_path)
    images.sort(key=lambda x: int(x[:-4]))  # 以名称字符串的数字从小到大排序　　
    fps = 20  # 帧数
    fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', 'V')
    im = Image.open(img_path + images[0])
    video_writer = cv2.VideoWriter(video_path, fourcc, fps, im.size)
    number = 0
    for img_i in images:
        number = number + 1
        frame = cv2.imread(img_path + img_i)
        print("\r", end="")  #顶天星科技进度条：
        print("Generate the final video: %d/%d"%(number-1,frame_count),"▋ " * round(30*number/frame_count),"- " * round(30*(frame_count-number)/frame_count),end="")
        video_writer.write(frame)  # 注意：图片尺寸必须和视频尺寸一样，不然不会被加入视频中！！！
    video_writer.release()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('video_name') 
    args = parser.parse_args()
    frame_count = read_video(args.video_name)
    change_pic(frame_count)
    char_to_img(frame_count)
    charts2video('char_img/','char_video.mp4',frame_count-1)
    shutil.rmtree('cache_pic')
    shutil.rmtree('char_img')
    print("\n the video is finished, called [char_video.mp4]")
   
