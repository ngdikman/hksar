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
            return True
        else:
            print(f"{url} 访问失败")
            return False
    except requests.RequestException:
        print(f"{url} 访问失败")
        return False

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
        # 替换m3u文件内容
        with open('$GITHUB_WORKSPACE/GDIPTV.m3u', 'r', encoding='utf-8') as file:
            content = file.read()

        # 定义正则表达式模式
        pattern = r'http://\d+\.\d+\.\d+\.\d+:\d+'
        # 定义替换字符串
        replacement = random.choice(channel_addresses)
        # 使用 re.sub 替换匹配的内容
        new_content = re.sub(pattern, f'http://{replacement}', content)

        # 写入修改后的内容到文件
        with open('GDIPTV.m3u', 'w', encoding='utf-8') as file:
            file.write(new_content)
else:
    print(f"请求失败，状态码: {response.status_code}")
