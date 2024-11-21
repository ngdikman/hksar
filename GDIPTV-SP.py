import requests
import re
import random

user_agent = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3100.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
        'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    ]

User_Agent = user_agent[random.randint(0, len(user_agent) - 1)]
headers = {
    'User-Agent': User_Agent
}

# 定义需要爬取的城市
urls = {"guangzhou":"https://fofa.info/result?qbase64=IlNlcnZlcjogdWRweHkiICYmIGNpdHk9Imd1YW5nemhvdSIgJiYgb3JnPSJDaGluYW5ldCI%3D",
        "jiangmen":"https://fofa.info/result?qbase64=IlNlcnZlcjogdWRweHkiICYmIGNpdHk9IkppYW5nbWVuIiAmJiBvcmc9IkNoaW5hbmV0Ig%3D%3D",
        "shantou":"https://fofa.info/result?qbase64=IlNlcnZlcjogdWRweHkiICYmIGNpdHk9InNoYW50b3UiICYmIG9yZz0iQ2hpbmFuZXQi",
        "shenzhen":"https://fofa.info/result?qbase64=IlNlcnZlcjogdWRweHkiICYmIGNpdHk9InNoZW56aGVuIiAmJiBvcmc9IkNoaW5hbmV0Ig%3D%3D",
        "dongguan":"https://fofa.info/result?qbase64=IlNlcnZlcjogdWRweHkiICYmIGNpdHk9ImRvbmdndWFuIiAmJiBvcmc9IkNoaW5hbmV0Ig%3D%3D",
        "qingyuan":"https://fofa.info/result?qbase64=IlNlcnZlcjogdWRweHkiICYmIGNpdHk9InFpbmd5dWFuIiAmJiBvcmc9IkNoaW5hbmV0Ig%3D%3D"
        }
urls_all = []

# 通过 Fofa 获取 IP 地址
for city, url in urls.items():
    try:
        response = requests.get(url, headers=headers, timeout=10)
        page_content = response.text
        print(f" {city} 访问成功")

        # 使用正则提取 IP 地址
        pattern = r'href="(http:\/\/\d+\.\d+\.\d+\.\d+:\d+)"'
        page_urls = re.findall(pattern, page_content)

        for urlx in page_urls:
            try:
                # 检测链接是否可用
                response = requests.get(url=f'{urlx}/status', timeout=10)
                response.raise_for_status() 
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

channel_addresses = urls_all
print(channel_addresses)

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
    existing_addresses = []  # 使用列表存储所有地址
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                address = line.strip()
                if address:
                    existing_addresses.append(address)  # 添加到列表
    except IOError:
        print(f"无法读取文件 {filename}")
    return existing_addresses

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
    all_addresses = channel_addresses + existing_addresses

    # 检测合并后的频道地址可用性
    valid_addresses = [addr for addr in all_addresses if test_m3u(addr)]

    # 保存有效的频道地址到文件
    save_addresses_to_file(valid_addresses, 'ip-port.txt')

    # 随机选择一个频道地址更新文件
    if valid_addresses:
        selected_address = random.choice(valid_addresses)
        replace_m3u_file('GDIPTV.m3u', selected_address)
        # replace_m3u_file('GDIPTV-SP.m3u', selected_address)
    else:
        print("没有可用的频道地址")

if __name__ == "__main__":
    main()
