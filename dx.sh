rm -rf ip/dianxin.onlygood.ip
city="dianxin"
# 使用城市名作为默认文件名，格式为 CityName.ip
ipfile="ip/${city}.ip"
only_good_ip="ip/${city}.onlygood.ip"

# 遍历 IP 并处理整个 IP 段（并发加速）
while IFS= read -r ip; do
    base_ip=$(echo "$ip" | awk -F: '{print $1}')
    port=$(echo "$ip" | awk -F: '{print $2}')
    
    seq 1 255 | xargs -P 50 -I {} bash -c '
        full_ip="'${base_ip%.*}'.{}:'$port'"
        tmp_ip=$(echo -n "$full_ip" | sed "s/:/ /")
        output=$(nc -w 1 -v -z $tmp_ip 2>&1)
        echo "$output"
        if [[ "$output" == *"succeeded"* ]]; then
            echo "$full_ip" >> "'$only_good_ip'"
        fi
    '
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
    url="http://$ip/udp/239.77.0.215:5146"
    echo "$url"
    curl "$url" --connect-timeout 3 --max-time 30 -o /dev/null >zubo.tmp 2>&1
    a=$(head -n 3 zubo.tmp | awk '{print $NF}' | tail -n 1)

    echo "第 $i/$lines 个：$ip $a"
    echo "$ip $a" >> "speedtest_${city}_$time.log"
done < "ip/${city}.onlygood.ip"

rm -f zubo.tmp
awk '/M|k/{print $2"  "$1}' "speedtest_${city}_$time.log" | sort -n -r >"result/result_fofa_${city}.txt"
cat "result/result_fofa_${city}.txt"
ip1=$(awk 'NR==1{print $2}' result/result_fofa_${city}.txt)
ip2=$(awk 'NR==2{print $2}' result/result_fofa_${city}.txt)
ip3=$(awk 'NR==3{print $2}' result/result_fofa_${city}.txt)
rm -f "speedtest_${city}_$time.log"

# 用 3 个最快 ip 生成对应城市的 m3u或txt
program="template/template_dx.m3u"
txtprogram="template/template_dx.txt"

# sed "s/ipipip/$ip1/g" "$program" > GDIPTV.m3u
# sed "s/ipipip/$ip2/g" "$program" > GDIPTV-SP.m3u

{
    head -1 "$program"
    prev_line=""
    tail -n +2 "$program" | while IFS= read -r line; do
        if [[ "$line" == \#EXTINF* ]]; then
            prev_line="$line"
        elif [[ "$line" == *ipipip* ]]; then
            for ip in "$ip1" "$ip2" "$ip3"; do
                [ -z "$ip" ] && continue
                echo "$prev_line"
                echo "$line" | sed "s/ipipip/$ip/g"
            done
        else
            echo "$line"
        fi
    done
} > GDIPTV.m3u

sed -e "s/ipipip/$ip1/g" -e "s/urlurlurl/$ip2/g" "$txtprogram" > "txt/fofa_${city}.txt"

rm -rf dianxin.txt
cat txt/fofa_dianxin.txt >> dianxin.txt

# 生成杂七杂八txt
# {
#   echo "📡 BXTV,#genre#"
#   curl -s "https://bxtv.3a.ink/live.txt" | grep -v '#genre#'
# } >> dianxin.txt

# {
#   curl -s "http://iptv.4666888.xyz/FYTV.txt" | sed 's/^.*#genre#/📡 &/'
# } >> dianxin.txt
