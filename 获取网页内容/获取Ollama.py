import requests
from bs4 import BeautifulSoup
import time
import random

# 创建一个会话对象
session = requests.Session()

# 设置请求头，模拟浏览器
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Cookie': 'isRedirectLang=1; is_mobile=pc; baseShowChange=false; viewOneHundredData=false; __fcd=ZIA5DSCCGRBGDPXH5CF4E9734E9E3B5C; befor_router=%2Fresult%3Fqbase64%3DaWNvbl9oYXNoPSItMTM1NDAyNzMxOSIgJiYgYXNuPSIxMzMzNSIgJiYgcG9ydD0iNDQzIg%253D%253D; fofa_token=eyJhbGciOiJIUzUxMiIsImtpZCI6Ik5XWTVZakF4TVRkalltSTJNRFZsWXpRM05EWXdaakF3TURVMlkyWTNZemd3TUdRd1pUTmpZUT09IiwidHlwIjoiSldUIn0.eyJpZCI6NjcyNDc4LCJtaWQiOjEwMDM5MDI2OSwidXNlcm5hbWUiOiLpo47mrYzmoqbov5wiLCJwYXJlbnRfaWQiOjAsImV4cCI6MTczOTcxMDM3OX0.Rg_Zruoo1twIfs5WZrz5za9QZ5K1Ivyv0B-vaGeXHLEqZylLHTuARCxJ_BjQKuczJatKBKWoD17ib6_A81ADtA; user=%7B%22id%22%3A672478%2C%22mid%22%3A100390269%2C%22is_admin%22%3Afalse%2C%22username%22%3A%22%E9%A3%8E%E6%AD%8C%E6%A2%A6%E8%BF%9C%22%2C%22nickname%22%3A%22%E9%A3%8E%E6%AD%8C%E6%A2%A6%E8%BF%9C%22%2C%22email%22%3A%22om2bg0face-rdtcsnqhb9opjpccs%40open_wechat%22%2C%22avatar_medium%22%3A%22https%3A%2F%2Fthirdwx.qlogo.cn%2Fmmopen%2Fvi_32%2FPiajxSqBRaELVH56tRm9ym3850NG3rJzVa7gTSoaDUfOXyC5fcibpy2jTLLSTPoly6ibfd1FdqzY3g8amxtPibDnelc7XoGBUZjhh0RicJUkFes13uUibUnzzcwg%2F132%22%2C%22avatar_thumb%22%3A%22https%3A%2F%2Fthirdwx.qlogo.cn%2Fmmopen%2Fvi_32%2FPiajxSqBRaELVH56tRm9ym3850NG3rJzVa7gTSoaDUfOXyC5fcibpy2jTLLSTPoly6ibfd1FdqzY3g8amxtPibDnelc7XoGBUZjhh0RicJUkFes13uUibUnzzcwg%2F132%22%2C%22key%22%3A%22772c6a34fabd78ff3d853fd5775aa314%22%2C%22category%22%3A%22user%22%2C%22rank_avatar%22%3A%22%22%2C%22rank_level%22%3A0%2C%22rank_name%22%3A%22%E6%B3%A8%E5%86%8C%E7%94%A8%E6%88%B7%22%2C%22company_name%22%3A%22%E9%A3%8E%E6%AD%8C%E6%A2%A6%E8%BF%9C%22%2C%22coins%22%3A0%2C%22can_pay_coins%22%3A0%2C%22fofa_point%22%3A0%2C%22credits%22%3A1%2C%22expiration%22%3A%22-%22%2C%22login_at%22%3A0%2C%22data_limit%22%3A%7B%22web_query%22%3A300%2C%22web_data%22%3A3000%2C%22api_query%22%3A0%2C%22api_data%22%3A0%2C%22data%22%3A-1%2C%22query%22%3A-1%7D%2C%22expiration_notice%22%3Afalse%2C%22remain_giveaway%22%3A1000%2C%22fpoint_upgrade%22%3Afalse%2C%22account_status%22%3A%22%22%2C%22parents_id%22%3A0%2C%22parents_email%22%3A%22%22%2C%22parents_fpoint%22%3A0%7D; is_flag_login=1'
}

# 目标URL
url = "https://fofa.info/result?qbase64=YXBwPSJPbGxhbWEiICYmIGNvdW50cnk9IkNOIiAmJiBpc19kb21haW49ZmFsc2UgJiYgcmVnaW9uPSJCZWlqaW5nIg%3D%3D"

# 发起请求
response = session.get(url, headers=headers)

# 检查请求是否成功
if response.status_code == 200:
    # 解析HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # 查找所有.hsxa-host下的a标签
    hsxa_host_divs = soup.find_all(class_='hsxa-host')
    for div in hsxa_host_divs:
        a_tags = div.find_all('a')
        for a in a_tags:
            print(a.get('href'))  # 输出a标签的href属性

    # 随机等待1到3秒之间
    time.sleep(random.uniform(1, 3))
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
