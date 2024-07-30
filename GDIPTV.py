import requests
from bs4 import BeautifulSoup
import random
import re

# 检测链接可用性
def test_m3u(url):
    try:
        response = requests.get(url=f'http://{url}/status', timeout=1)
        if response.status_code == 200:
            print(f"{url} 访问成功")
            return url
        else:
            #print(f"{url} 访问失败")
            return None
    except requests.RequestException:
        #print(f"{url} 访问失败")
        return None

# 从http://tonkiang.us/爬链接
url = 'http://tonkiang.us/hoteliptv.php'
data = {'saerch': '广东电信'}
session = requests.Session()
response = session.post(url, data=data)

# 确保请求成功
if response.status_code == 200:
    # 解析HTML内容
    soup = BeautifulSoup(response.text, 'html.parser')
    # 找到所有符合条件的div
    channels = []
    for div in soup.find_all('div', class_='channel'):
        sibling_div = div.find_next_sibling('div', style="float: right; ")
        if sibling_div:
            sub_div = sibling_div.find('div', style="color:limegreen; ")
            if sub_div:
                channels.append(div)

    channel_addresses = []
    # 输出符合条件的div下b标签的文本
    for channel in channels:
        b_tag = channel.find('b')
        if b_tag:
            channel_address = b_tag.get_text().strip()
            if test_m3u(channel_address):
                channel_addresses.append(channel_address)

    if not channel_addresses:
        print("没有可用的频道地址")
    else:
        # 定义正则表达式模式
        pattern = r'http://[\w]+.[\w]+.[\w]+.[\w]+:[\w]+'
        # 替换内容的函数
        def replace_m3u_file(filename):
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
                print(f"读取 {filename} 文件成功")

            # 定义替换字符串
            replacement = random.choice(channel_addresses)
            # 使用 re.sub 替换匹配的内容
            new_content = re.sub(pattern, f'http://{replacement}', content)

            # 写入修改后的内容到文件
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(new_content)
                print(f"写入 {filename} 文件成功")

        # 处理 GDIPTV.m3u 文件
        replace_m3u_file('GDIPTV.m3u')
        # 处理 GDIPTV-SP.m3u 文件
        replace_m3u_file('GDIPTV-SP.m3u')

else:
    print(f"请求失败，状态码: {response.status_code}")
