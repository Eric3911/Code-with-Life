# python多线程下载图像

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import io
import os
import urllib3
import multiprocessing

from PIL import Image
from tqdm import tqdm
from urllib3.util import Retry

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def download_image(filenames_and_urls):
    """
    下载图片，并以 90% 质量保存为 JPG 格式.
    如果图片已存在，则自动跳过.
    """
    fname, url = filenames_and_urls
    if not os.path.exists(fname):
        http = urllib3.PoolManager(retries=Retry(connect=3, read=2, redirect=3))
        response = http.request("GET", url)
        image = Image.open(io.BytesIO(response.data))
        image_rgb = image.convert("RGB")
        image_rgb.save(fname, format='JPEG', quality=90)
    

if __name__ == '__main__':
    print("[INFO]多进程下载图片")
    
    # 读取 filenames 和 urls
    # filenames_urls = (filenames, urls)

    # 图片下载
    pool = multiprocessing.Pool(processes=12)
    with tqdm(total=len(fnames_urls)) as progress_bar:
        for _ in pool.imap_unordered(download_image, filenames_urls):
            progress_bar.update(1)

    print("[INFO]Done.")