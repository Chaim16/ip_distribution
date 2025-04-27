import os
import traceback
import random

import requests
from bs4 import BeautifulSoup

# 创建保存图片的文件夹
save_dir = "D:/crawler"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

def get_image_urls(page=1, size=10):
    urls = []
    while size:
        random_num = random.randint(1, 10000)
        url = "https://picsum.photos/1600/900?random={}".format(random_num)
        urls.append(url)
        size -= 1
    return urls


# 下载并保存图片
def download_images(img_urls):
    count = 0
    for img_url in img_urls:
        try:
            img_data = requests.get(img_url).content
            img_name = os.path.join(save_dir, f"image_{count + 1}.jpg")
            with open(img_name, 'wb') as f:
                f.write(img_data)
            print(f"保存图片: {img_name}")
            count += 1
        except Exception as e:
            print(f"下载图片失败: {e}")


if __name__ == '__main__':
    try:
        # 获取图片链接
        img_urls = get_image_urls(1, 10)
        print(img_urls)

        # 下载前10张图片
        download_images(img_urls)
    except Exception as e:
        print(traceback.format_exc())



