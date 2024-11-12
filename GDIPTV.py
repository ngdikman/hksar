import requests
from bs4 import BeautifulSoup
import random
import re

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

# 替换M3U文件中的URL
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

# 爬取链接
def fetch_channels(base_url, search_term):
    session = requests.Session()
    response = session.post(base_url, data={saerch: search_term})

    if response.status_code != 200:
        print(f"请求失败，状态码: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    channels = []
    for div in soup.find_all('div', class_='channel'):
        sibling_div = div.find_next_sibling('div', style="float: right; ")
        if sibling_div:
            sub_div = sibling_div.find('div', style="color:limegreen; ")
            if sub_div:
                channels.append(div)
    return channels

# 获取符合条件的频道地址列表
def get_channel_addresses(channels):
    channel_addresses = []
    for channel in channels:
        b_tag = channel.find('b')
        if b_tag:
            channel_address = b_tag.get_text().strip()
            if test_m3u(channel_address):
                channel_addresses.append(channel_address)
    return channel_addresses

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
    base_url = 'http://tonkiang.us/hoteliptv.php'
    search_term = '广东电信'

    # 爬取新的频道数据
    channels = fetch_channels(base_url, search_term)
    new_channel_addresses = get_channel_addresses(channels)

    # 从文件读取已有的频道地址
    existing_addresses = read_addresses_from_file('ip-port.txt')

    # 合并新的和已有的频道地址并去重
    all_addresses = set(new_channel_addresses) | existing_addresses

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
