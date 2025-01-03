import requests
from bs4 import BeautifulSoup

# 访问网址
url = 'https://cf.090227.xyz/'

# 模拟浏览器的请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = requests.get(url, headers=headers)

# 解析网页内容
soup = BeautifulSoup(response.content, 'html.parser')

# 找到class="centered"的div
centered_div = soup.find('div', class_='centered')

# 在div中找到table
table = centered_div.find('table')

# 提取table前10个tr中的td数据，并将结果写入txt文件
with open('results.txt', 'w', encoding='utf-8') as file:
    rows = table.find_all('tr')[:10]
    for row in rows:
        cells = row.find_all('td')
        if len(cells) >= 5:
            service_provider = cells[0].text.strip()
            ip_address = cells[1].text.strip()
            latency = cells[2].text.strip()
            packet_loss = cells[3].text.strip()
            speed = cells[4].text.strip()

            formatted_output = f'服务商：{service_provider}，IP：{ip_address}，延迟：{latency}，丢包率：{packet_loss}，速度：{speed}\n'
            file.write(formatted_output)
