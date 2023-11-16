from playwright.sync_api import Playwright, sync_playwright
import time
import clipboard
import json
import requests

USER_ID = 'l0722l@naver.com'
USER_PW = 'dlwhdtjs2'

def run(playwright: Playwright) -> None:
    # chrome 브라우저를 실행
    browser = playwright.chromium.launch()
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    page.goto("https://accounts.kakao.com/login/?continue=https%3A%2F%2Fkauth.kakao.com%2Foauth%2Fauthorize%3Fproxy%3DeasyXDM_Kakao_478vz51xwq_provider%26ka%3Dsdk%252F1.43.1%2520os%252Fjavascript%2520sdk_type%252Fjavascript%2520lang%252Fko-KR%2520device%252FWin32%2520origin%252Fhttps%25253A%25252F%25252Fpartners.newspic.kr%26origin%3Dhttps%253A%252F%252Fpartners.newspic.kr%26response_type%3Dcode%26redirect_uri%3Dkakaojs%26state%3Dohcis0fxg1slexiy4avgc%26through_account%3Dtrue%26client_id%3Ddafaf71bd4bbaa5f108c01a16509395e&talk_login=hidden#login")
    page.click("#loginId--1")
    page.fill("#loginId--1", USER_ID)
    page.press("#loginId--1", "Tab")
    page.fill("#password--2", USER_PW)
    page.press("#password--2", "Tab")

    # Press Enter
    with page.expect_navigation():
        page.press("text=로그인", "Enter")

    page.goto(url="https://partners.newspic.kr/login")
    with page.expect_navigation():
        page.press("text=카카오톡으로 로그인", "Enter")
        
    page.goto(url="https://partners.newspic.kr/category/categoryDetail?channelNo=89&subChannelNo=91")
    time.sleep(1)
    news_list = page.query_selector_all("#categoryList > li")
    
    news_json = []
    
    i = 0
    for news in news_list:
        news_info={}
        news_info["img"] = news.query_selector("div.thumb > img").get_attribute("src")
        news_info["title"] = news.query_selector("div.info > a > span").text_content()
        news.query_selector("div.thumb > img").click()
        news.query_selector("div.thumb > div.box-share > ul > li:nth-child(1) > button").click()
        news_info["link"] = clipboard.paste()
        
        news_json.append(news_info)
        
    context.close()
    browser.close()
    
    file_path = './newspic.json'
    
    with open(file_path, 'w') as file:
        json.dump(news_json, file)
    
    print("완료")


with sync_playwright() as playwright:
    run(playwright)
