rm -rf ip/dianxin.onlygood.ip
city="dianxin"
# 使用城市名作为默认文件名，格式为 CityName.ip
ipfile="ip/${city}.ip"
only_good_ip="ip/${city}.onlygood.ip"
# 遍历文件 A 中的每个 IP 地址
while IFS= read -r ip; do
    # 尝试连接 IP 地址和端口号，并将输出保存到变量中
    tmp_ip=$(echo -n "$ip" | sed 's/:/ /')
    echo "nc -w 1 -v -z $tmp_ip 2>&1"
    output=$(nc -w 1 -v -z $tmp_ip 2>&1)
    echo $output    
    # 如果连接成功，且输出包含 "succeeded"，则将结果保存到输出文件中
    if [[ $output == *"succeeded"* ]]; then
        # 使用 awk 提取 IP 地址和端口号对应的字符串，并保存到输出文件中
        echo "$output" | grep "succeeded" | awk -v ip="$ip" '{print ip}' >> "ip/${city}.onlygood.ip"
    fi
done < "$ipfile"
echo "===============检索完成================="

# 检查文件是否存在
if [ ! -f "ip/${city}.onlygood.ip" ]; then
    echo "错误：文件 ip/${city}.onlygood.ip 不存在。"
    exit 1
fi


lines=$(wc -l < "ip/${city}.onlygood.ip")
echo "【ip/${city}.onlygood.ip】内 ip 共计 $lines 个"

i=0
time=$(date +%Y%m%d%H%M%S) # 定义 time 变量
while IFS= read -r line; do
    i=$((i + 1))
    ip="$line"
    url="http://$ip/udp/239.77.0.114:5146"
    echo "$url"
    curl "$url" --connect-timeout 3 --max-time 10 -o /dev/null >zubo.tmp 2>&1
    a=$(head -n 3 zubo.tmp | awk '{print $NF}' | tail -n 1)

    echo "第 $i/$lines 个：$ip $a"
    echo "$ip $a" >> "speedtest_${city}_$time.log"
done < "ip/${city}.onlygood.ip"

rm -f zubo.tmp
awk '/M|k/{print $2"  "$1}' "speedtest_${city}_$time.log" | sort -n -r >"result_fofa_${city}.txt"
cat "result_fofa_${city}.txt"
ip1=$(awk 'NR==1{print $2}' result_fofa_${city}.txt)
ip2=$(awk 'NR==2{print $2}' result_fofa_${city}.txt)
#ip3=$(awk 'NR==3{print $2}' result_fofa_${city}.txt)
rm -f "speedtest_${city}_$time.log"

# 用 3 个最快 ip 生成对应城市的 txt 文件
program="template/template_GDIPTV.m3u"

sed "s/ipipip/$ip1/g" "$program" > tmp1.txt
sed "s/ipipip/$ip2/g" "$program" > tmp2.txt
#sed "s/ipipip/$ip3/g" "$program" > tmp3.txt
cat tmp1.txt > "GDIPTV.m3u"
cat tmp2.txt > "GDIPTV-SP.m3u"
rm -rf tmp1.txt tmp2.txt tmp3.txt
