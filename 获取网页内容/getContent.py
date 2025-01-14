import requests

url = "https://api.4chat.me/v1/models"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/115.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,"
              "application/xml;q=0.9,image/avif,image/webp,"
              "image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "zh-CN,zh;q=0.9",
    # 移除 br，以避免brotli压缩
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    # 如果响应是JSON格式，可以直接解析
    data = response.json()
    import json
    print(json.dumps(data, indent=4, ensure_ascii=False))
except requests.exceptions.HTTPError as err:
    print(f"HTTP错误：{err}")
except requests.exceptions.RequestException as e:
    print(f"请求异常：{e}")
except ValueError:
    print("响应内容不是有效的JSON格式")
