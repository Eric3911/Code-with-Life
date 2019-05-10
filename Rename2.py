#conding: utf-8-
#Author:'Jungang'
#Time:2019/5/10

#训练图像数据重命名代码

import os

path = 'E:\\ca\\'

filelist = os.listdir(path)
count = 0

for file in filelist:
    olddir = os.path.join(path,file)
    if os.path.isdir(olddir):
        continue
    filename = os.path.splitext(file)[0]
    filetype = os.path.splitext(file)[1]
	
#****************************************名称总长位数4********
    Newdir = os.path.join(path,str(count).zfill(4)+filetype)
    os.rename(olddir,Newdir)

    count += 1
