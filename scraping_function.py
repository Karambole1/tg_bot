import requests
from bs4 import BeautifulSoup


def scrap(url, class_to_scrap):

    headers = {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
    }

    req = requests.get(url, headers=headers)
    src = req.text

    soup = BeautifulSoup(src, "lxml")
    course = soup.find(class_=class_to_scrap)
    return course.text.replace(',', '.')


# scrap("https://www.bybit.com/ru-RU/trade/spot/APT/USDT", "label color-buy")
