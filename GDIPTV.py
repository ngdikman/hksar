import requests
from bs4 import BeautifulSoup
import random
import re
import subprocess
# 获取IPTV播放速度信息（酒店源m3u等和组播源皆可用）
def get_ffmpeg_speed(url):
    try:
        modified_url = f"http://{url}/udp/239.77.1.19:5146"

        # 测试或超时时长/秒
        delay = 10
        # 构建FFmpeg命令
        ffmpeg_command = f"ffmpeg -i {modified_url} -t {delay} -f null -"

        # 执行FFmpeg命令并捕获输出
        process = subprocess.Popen(ffmpeg_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(timeout=20)

        # 从FFmpeg输出中提取下载速度
        output_str = stderr.decode("utf-8")
        match = re.findall(r'speed=(.*?)x', output_str)

        if match:
            # 计算速度数组的平均值
            speeds = [float(speed) for speed in match]
            avg_speed_mbps = sum(speeds) / len(speeds)
            speed_mbps = float('{:.2f}'.format(avg_speed_mbps))
            speed_mbps = 0.00 if speed_mbps < 0.50 else speed_mbps
        else:
            speed_mbps = 0.00

        return speed_mbps
    except subprocess.CalledProcessError as e:
        return None
    except re.error as e:
        return None
    except Exception as e:
        return None

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
            speed = get_ffmpeg_speed(channel_address)
            if speed and speed > 0:
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
