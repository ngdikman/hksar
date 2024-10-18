import requests
import random
import re
import base64

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
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Cookie':'isRedirectLang=1; is_mobile=pc; __fcd=VbD24BtuzdjmUosS9FcCivXF; befor_router=%2Fresult%3Fqbase64%3DIlNlcnZlcjogdWRweHkiICYmIGNpdHk9Imd1YW5nemhvdSIgJiYgb3JnPSJDaGluYW5ldCI%253D; fofa_token=eyJhbGciOiJIUzUxMiIsImtpZCI6Ik5XWTVZakF4TVRkalltSTJNRFZsWXpRM05EWXdaakF3TURVMlkyWTNZemd3TUdRd1pUTmpZUT09IiwidHlwIjoiSldUIn0.eyJpZCI6NDcyMjA0LCJtaWQiOjEwMDI3MTkwMywidXNlcm5hbWUiOiJuZ2Rpa21hbiIsInBhcmVudF9pZCI6MCwiZXhwIjoxNzI5NDkwNjE0fQ.2AMheJtRyaIKkYuhWEUBf7j3Qtii9T_7M_cZWZXlV2U2qA8FX9tKCgYInAen40-yv2Duh7r12IzHWZiNIZmEyQ; user=%7B%22id%22%3A472204%2C%22mid%22%3A100271903%2C%22is_admin%22%3Afalse%2C%22username%22%3A%22ngdikman%22%2C%22nickname%22%3A%22ngdikman%22%2C%22email%22%3A%22373025846%40qq.com%22%2C%22avatar_medium%22%3A%22https%3A%2F%2Fnosec.org%2Fmissing.jpg%22%2C%22avatar_thumb%22%3A%22https%3A%2F%2Fnosec.org%2Fmissing.jpg%22%2C%22key%22%3A%228e14b553abf0330d4c59b9533db34847%22%2C%22category%22%3A%22user%22%2C%22rank_avatar%22%3A%22%22%2C%22rank_level%22%3A0%2C%22rank_name%22%3A%22%E6%B3%A8%E5%86%8C%E7%94%A8%E6%88%B7%22%2C%22company_name%22%3A%22ngdikman%22%2C%22coins%22%3A0%2C%22can_pay_coins%22%3A0%2C%22fofa_point%22%3A0%2C%22credits%22%3A1%2C%22expiration%22%3A%22-%22%2C%22login_at%22%3A0%2C%22data_limit%22%3A%7B%22web_query%22%3A300%2C%22web_data%22%3A3000%2C%22api_query%22%3A0%2C%22api_data%22%3A0%2C%22data%22%3A-1%2C%22query%22%3A-1%7D%2C%22expiration_notice%22%3Afalse%2C%22remain_giveaway%22%3A0%2C%22fpoint_upgrade%22%3Afalse%2C%22account_status%22%3A%22%22%2C%22parents_id%22%3A0%2C%22parents_email%22%3A%22%22%2C%22parents_fpoint%22%3A0%7D; is_flag_login=1; baseShowChange=false; viewOneHundredData=false'}
# urls = ["guangzhou"]
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
    # replace_m3u_file('GDIPTV-SP.m3u')
