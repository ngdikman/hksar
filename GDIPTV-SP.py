import requests
import random
import re
import base64
import os

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

# 爬链接
cookie = os.getenv("FOFA_COOKIE")
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Authorization':cookie
}
urls = ["guangzhou","jiangmen","shantou","shenzhen","dongguan","qingyuan"]
urls_all = []
for url in urls:
    url_0 = str(base64.b64encode((f'"Server: udpxy" && city="{url}" && org="Chinanet"').encode("utf-8")), "utf-8")
    url_64 =f'https://fofa.info/result?qbase64={url_0}'
    try:
        response = requests.get(url_64, headers=headers, timeout = 15)
        page_content = response.text
        print(f" {url}  访问成功")
        pattern = r'href="(http://\d+\.\d+\.\d+\.\d+:\d+)"'
        page_urls = re.findall(pattern, page_content)
        for urlx in page_urls:
            try:
                response = requests.get(url=urlx+'/status', timeout=1)
                response.raise_for_status()  # 返回状态码不是200异常
                page_content = response.text
                pattern = r'class="proctabl"'
                page_proctabl = re.findall(pattern, page_content)
                if page_proctabl:
                    urls_all.append(urlx)
                    print(f" {urlx}  访问成功")
            except requests.RequestException as e:
                pass
    except:
        #print(f" {url}  访问失败")
        pass

channel_addresses = list(set(urls_all))  # 去重得到唯一的URL列表
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
        new_content = re.sub(pattern, f'{replacement}', content)

        # 写入修改后的内容到文件
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(new_content)
            print(f"写入 {filename} 文件成功")

    # 处理 GDIPTV.m3u 文件
    replace_m3u_file('GDIPTV.m3u')
    # 处理 GDIPTV-SP.m3u 文件
    replace_m3u_file('GDIPTV-SP.m3u')
