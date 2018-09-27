#导入相关库函数
import itchat
import math
import os
import PIL.Image as Image
from os import listdir
import urllib
import requests
import numpy as np
import pandas as pd
from collections import defaultdict
import re
import matplotlib.pyplot as plt
import jieba
from wordcloud import WordCloud


#登陆微信
itchat.auto_login()
friends = itchat.get_friends(update=True)[0:]

#统计好友数量
MyName=friends[0].NickName
file = '\%s'%MyName
cp = os.getcwd()
path = os.path.join(cp + file)
os.chdir(path)
number_of_friends = len(friends)
print("好友总数:" + str(number_of_friends))
filename = 'pachong.txt'
with open(filename,'w') as file_object:
	file_object.write("------------------------------------------")
	file_object.write("\n好友总数:" + str(number_of_friends))

#统计好友性别比例
df_friends = pd.DataFrame(friends)
Sex=df_friends.Sex
Sex_count=Sex.value_counts()
Sex_count2=Sex.value_counts()
print(Sex_count2)
#画出男女比例柱形图
plt.figure('好友性别')
Sex_count.plot(kind='bar')
plt.title('friends sex bar')
plt.xlabel('sex')
plt.ylabel('numbers')
plt.ylim((0,100))
new_ticks=np.linspace(0,100,5)
plt.yticks(new_ticks)
plt.xticks([2,1,0],
           ['unknow','female','male'])
plt.xticks(rotation=360)

plt.savefig('./filebar.jpg',format='jpg')
plt.show()



# 提取签名，得到语料库
Signatures = df_friends.Signature
regex1 = re.compile('<span.*?</span>') #匹配表情
regex2 = re.compile('\s{2,}')#匹配两个以上占位符。
Signatures = [regex2.sub(' ',regex1.sub('',signature,re.S)) for signature in Signatures] #用一个空格替换表情和多个空格。
Signatures = [signature for signature in Signatures if len(signature)>0] #去除空字符串
text = ' '.join(Signatures)
file_name = MyName+'_wechat_signatures.txt'
#读取文件内容
word_content=open(file_name,'r',encoding='utf-8').read().replace('\n','')
#进行分词
word_cut=jieba.cut(word_content)
#把分词用空格连起来
word_cut_join=" ".join(word_cut)
#画图
img=Image.open("C:\\Users\\Administrator\\Pictures\\ciyunpic.png")
graph = np.array(img) #词云的背景和颜色。这张图片在本地。
my_wordcloud = WordCloud(background_color="white",
                         max_words=2000,
                         max_font_size=60,
                         random_state=42,
                          scale=2,
                         mask=graph,  
                         font_path="C:\Windows\Fonts\simkai.ttf").generate(word_cut_join) #生成词云。

plt.imshow(my_wordcloud)
plt.axis('off')
plt.show()
file_name_p = MyName+'.jpg'
my_wordcloud.to_file(file_name_p) #保存图片


#下载微信好友头像并完成拼接
num = 0
for i in friends:
	img = itchat.get_head_img(userName=i["UserName"])
	fileImage = open(user + "/" + str(num) + ".jpg",'wb')
	fileImage.write(img)
	fileImage.close()
	num += 1
	
user = friends[0]["UserName"]
os.mkdir(user)
pics = listdir(user)
numPic = len(pics)
print("图片数量：" + str(numPic))
eachsize = int(math.sqrt(float(640 * 640) / numPic))#每张照片的大小
print("每张照片的大小：",eachsize)
numline = int(640 / eachsize)#每行照片数量
print("每行照片数量",numline)
image_new = Image.new('RGBA', (640, 640))
x = 0
y = 0
for i in pics:
	    img = Image.open(user + "/" + i) #打开图片
        img = img.resize((eachsize, eachsize), Image.ANTIALIAS)#缩小图片
		image_new.paste(img, (x * eachsize, y * eachsize))
		x += 1
		if x == numline:
			x = 0
			y += 1
	
image_new=image_new.convert("P")#将RGB图片转为像素在（0，255）之间的彩色图片，因为RGB格式一般软件不支持，需要转为以半年格式
image_new.show()
image_new.save("user.JPG")
itchat.send_image(user + ".jpg", 'filehelper')
