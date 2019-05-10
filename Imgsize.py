#conding: utf-8-
#Author:'Jungang'
#Time:2019/5/8


from PIL import Image
import os.path
import glob

def convertjpg(jpgfile,outdir, width=320,height=240 ):
    img=Image.open(jpgfile)
    try:


        new_img=img.resize((width,height),Image.BILINEAR)
        new_img.save(os.path.join(outdir,os.path.basename(jpgfile)))


    except Exception as e:
        print(e)
for jpgfile in glob.glob("E:/ca/*.jpg"):
    convertjpg(jpgfile,"E:/ca/")

