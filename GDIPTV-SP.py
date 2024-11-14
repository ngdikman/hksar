import requests
import re
import random
import base64
import os

cookie = os.getenv("FOFA_COOKIE")
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Authorization':cookie
}

# 定义需要爬取的城市
urls = ["guangzhou", "jiangmen", "shantou", "shenzhen", "dongguan", "qingyuan"]
urls_all = []

# 通过 Fofa 获取 IP 地址
for url in urls:
    url_0 = str(base64.b64encode((f'"Server: udpxy" && city="{url}" && org="Chinanet"').encode("utf-8")), "utf-8")
    url_64 = f'https://fofa.info/result?qbase64={url_0}'

    try:
        response = requests.get(url_64, headers=headers, timeout=15)
        page_content = response.text
        print(f" {url} 访问成功")

        # 使用正则提取 IP 地址
        pattern = r'href="(http://\d+\.\d+\.\d+\.\d+:\d+)"'
        page_urls = re.findall(pattern, page_content)

        for urlx in page_urls:
            try:
                # 检测链接是否可用
                response = requests.get(url=f'{urlx}/status', timeout=1)
                response.raise_for_status()  # 如果状态码不是 200 会引发异常
                page_content = response.text

                # 判断页面是否包含有效的内容
                pattern = r'class="proctabl"'
                page_proctabl = re.findall(pattern, page_content)
                if page_proctabl:
                    urls_all.append(urlx)
                    print(f" {urlx} 访问成功")
            except requests.RequestException:
                pass

    except requests.RequestException:
        pass

# 去重获取到的 IP 地址
channel_addresses = list(set(urls_all))
if not channel_addresses:
    print("没有可用的频道地址")

# M3U 文件 URL 替换逻辑
url_pattern = re.compile(r'http://[\w.]+:[\d]+')

# 检测链接可用性
def test_m3u(url):
    try:
        response = requests.get(url=f'http://{url}/status', timeout=1)
        if response.status_code == 200:
            print(f"{url} 访问成功")
            return url
        else:
            return None
    except requests.RequestException:
        return None

# 替换 M3U 文件中的 URL
def replace_m3u_file(filename, replacement_url):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        new_content = url_pattern.sub(f'http://{replacement_url}', content)

        with open(filename, 'w', encoding='utf-8') as file:
            file.write(new_content)
            print(f"成功更新文件 {filename}")
    except IOError:
        print(f"无法处理文件 {filename}")

# 从文件中读取频道地址
def read_addresses_from_file(filename='ip-port.txt'):
    addresses = set()  # 使用集合去重
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                address = line.strip()
                if address:
                    addresses.add(address)
    except IOError:
        print(f"无法读取文件 {filename}")
    return addresses

# 保存频道地址到文件
def save_addresses_to_file(channel_addresses, filename='ip-port.txt'):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            for address in channel_addresses:
                file.write(f"{address}\n")
        print(f"频道地址已保存到 {filename}")
    except IOError:
        print(f"无法写入文件 {filename}")

# 主函数逻辑
def main():
    # 合并新的和已有的频道地址并去重
    existing_addresses = read_addresses_from_file('ip-port.txt')
    all_addresses = set(channel_addresses) | existing_addresses

    # 检测合并后的频道地址可用性
    valid_addresses = [addr for addr in all_addresses if test_m3u(addr)]

    # 保存有效的频道地址到文件
    save_addresses_to_file(valid_addresses, 'ip-port.txt')

    # 随机选择一个频道地址更新文件
    if valid_addresses:
        selected_address = random.choice(valid_addresses)
        replace_m3u_file('GDIPTV.m3u', selected_address)
        replace_m3u_file('GDIPTV-SP.m3u', selected_address)
    else:
        print("没有可用的频道地址")

if __name__ == "__main__":
    main()
