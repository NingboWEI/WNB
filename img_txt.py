from PIL import Image
import argparse

#read a picture and generate a txt file
# 首先，构建命令行输入参数处理 ArgumentParser 实例
parser = argparse.ArgumentParser()

# 定义输入文件、输出文件、输出字符画的宽和高
parser.add_argument('file')     #输入文件
parser.add_argument('-o', '--output')   #输出文件
parser.add_argument('--width', type = int, default = 977) #输出字符画宽
parser.add_argument('--height', type = int, default = 230) #输出字符画高

# 解析并获取参数
args = parser.parse_args()
# 输入的图片文件路径
IMG = args.file
# 输出字符画的宽度
WIDTH = args.width
# 输出字符画的高度
HEIGHT = args.height
# 输出字符画的路径
OUTPUT = args.output

ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")


# 将256灰度映射到70个字符上
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


if __name__ == '__main__':
    
    # 打开并调整图片的宽和高
    im = Image.open(IMG)
    real_width, real_height = im.size
    rate = real_height/real_width
    print("get the picture with size: %d * %d, rate is %f"%(real_width,real_height,rate)) 
    WIDTH = round(1.9*HEIGHT/rate)
    im = im.resize((WIDTH,HEIGHT), Image.NEAREST)#HEIGHT will keep at 359

    # 初始化输出的字符串
    txt = ""
    
    # 遍历图片中的每一行
    for i in range(HEIGHT):
        # 遍历该行中的每一列
        for j in range(WIDTH):
            # 将 (j,i) 坐标的 RGB 像素转为字符后添加到 txt 字符串
            txt += get_char(*im.getpixel((j,i)))
        # 遍历完一行后需要增加换行符
        txt += '\n'
    # 输出到屏幕
    print("loading...")
    
    # 字符画输出到文件
    if OUTPUT:
        with open(OUTPUT,'w') as f:
            f.write(txt)
    else:
        with open("output.txt",'w') as f:
            f.write(txt)   
    print("ready!!! The height is %d and the width is %d"%(HEIGHT,WIDTH)) 
    # print(HEIGHT) 
    # print(" and the width is ") 
    # print(WIDTH)
