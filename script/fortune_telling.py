import os
import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from dotenv import load_dotenv


load_dotenv(override=True)

jiyoon_base_url = "https://askjiyun.com/?mid=today&page={}"
jiyoon_headers = {
    "Accept": "text/html",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

slack_webhook = os.getenv("SLACK_LUCKY_DAILY")
slack_headers = {
    "Content-type": "application/json"
}

kw_webhook = os.getenv("KW_LUCKY_DAILY")
kw_headers = {
    "Content-type": "application/json"
}

def fetch_today(today):
    
    data = ""
    
    page = 1
    while True:     
        
        # 오늘의 운세 URL 조회
        response = requests.get(
            jiyoon_base_url.format(page),
            headers=jiyoon_headers
        )

        if response.status_code != 200:
            return f"ERROR: {response.status_code} {response.text}"

        soup = BeautifulSoup(response.text, "html.parser")

        today_a_line = soup.find("a", string=lambda text: text and today in text)
        
        if today_a_line is not None:
            break
        
        if page == 5:   # 5페이지 이내에서만 오늘 날짜를 검색
            break
        page += 1
        
    today_a_href = today_a_line.get("href")     # 오늘의 운세 게시글 링크
    
    # 오늘의 운세 조회
    response = requests.get(
        today_a_href,
        headers=jiyoon_headers
    )

    if response.status_code != 200:
        return f"ERROR: {response.status_code} {response.text}"

    soup = BeautifulSoup(response.text, "html.parser")

    p_list = soup.find("div", class_="contentBody").find_all("p")

    for p in p_list:
        data += p.text + "\n"

    return data


def send_slack(data):
    
    response = requests.post(
        slack_webhook,
        headers=slack_headers,
        data=json.dumps({
            "text": data
        })
    )
    
    if response.status_code != 200:
        return f"ERROR: {response.status_code} {response.text}"

    return


def send_kw(data):

    response = requests.post(
        kw_webhook,
        headers=kw_headers,
        data=json.dumps({
            "text": data
        })
    )
    
    if response.status_code != 200:
        return f"ERROR: {response.status_coƒde} {response.text}"

    return


if __name__ == "__main__":

    now = datetime.today()
    today = now.strftime("%-m월 %-d일")

    fortune_data = fetch_today(today)

    send_slack(fortune_data)
    send_kw(fortune_data)
