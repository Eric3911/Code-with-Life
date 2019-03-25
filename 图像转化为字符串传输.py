# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 09:26:58 2019

@author: Administrator
"""

# 1、将图片转为Base64编码

import base64

with open('C:\\Users\\Administrator\\Desktop\\pic\\mask\\Mark\\An.png','rb') as f:
    base64_data = base64.b64encode(f.read())
    s = base64_data.decode()
    print('data:image/jpeg;base64,%s'%s)
    