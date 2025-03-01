import os
import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from dotenv import load_dotenv


if os.path.exists("../.env"):
    load_dotenv(override=True)

jiyoon_base_url = "https://askjiyun.com/today"
jiyoon_headers = {
    "Accept": "text/html",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

slack_webhook = os.getenv("SLACK_LUCKY_DAILY")
slack_headers = {
    "Content-type": "application/json"
}

def fetch_today(today):
    
    data = ""
    
    # 오늘의 운세 URL 조회
    response = requests.get(
        jiyoon_base_url,
        headers=jiyoon_headers
    )

    if response.status_code != 200:
        return f"ERROR: {response.status_code} {response.text}"

    soup = BeautifulSoup(response.text, "html.parser")
    
    today_a_line = soup.find("a", string=lambda text: text and today in text)
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
    
    print(slack_webhook)
    # response = requests.post(
    #     slack_webhook,
    #     headers=slack_headers,
    #     data=json.dumps({
    #         "text": data
    #     })
    # )
    
    # if response.status_code != 200:
    #     return f"ERROR: {response.status_code} {response.text}"

    return


if __name__ == "__main__":

    now = datetime.today()
    today = now.strftime("%-m월 %-d일")

    send_slack(fetch_today(today))
