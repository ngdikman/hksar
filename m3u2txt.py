def process_m3u(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # 过滤掉M3U文件中的空行
            lines = [line.strip() for line in lines if line.strip() and not line.startswith('#EXTM3U')]
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for line in lines:
                if line.startswith('#EXTINF'):
                    # 获取含有#EXTINF的行中最后一个英文逗号后的文字
                    info = line.split(',')[-1]
                    f.write(info.strip() + ',')
                else:
                    f.write(line + '\n')

        print("转换完成！")
    except Exception as e:
        print("发生错误：", e)

# 使用示例
input_file = 'GDIPTV.m3u'
output_file = 'GDIPTV.txt'
process_m3u(input_file, output_file)
