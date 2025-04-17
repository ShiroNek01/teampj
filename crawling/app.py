import time
import random
import json 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options #네이버는 자동화된 접근을 막기에 브라우저처럼 보이게하는 설정의 헤더파일
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import chromedriver_autoinstaller

chromedriver_autoinstaller.install()

#네이버는 자동화된 접근을 막기에 브라우저처럼 보이게하는 설정
options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
driver = webdriver.Chrome(options=options)

#네이버 지도 열기
driver.get("https://map.naver.com/v5") #get() 원하는 링크로 이동
time.sleep(random.uniform(2,5))

#검색창 요소 찾기
search_input = driver.find_element(By.CLASS_NAME, "input_search")
search_input.send_keys("괴정동 맛집")
search_input.send_keys(Keys.ENTER)

time.sleep(2)

#searchIframe으로 이동
try:
    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "searchIframe"))
    )
except:
    print('에러')
    driver.quit()
    exit()

#검색 결과 요소 가져오기
try:
    place_list = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "TYaxT"))
    )
    print(f"{len(place_list)}")
except:
    print("요소 찾을 수 없음")
    driver.quit()
    exit()

place_info = {}

if place_list:
    for i in range(7):
        place_name = place_list[i].text.strip()
        place_info[place_name] = {"review": []}

        #부모 요소를 클릭(자식 요소를 클릭할 경우 텍스트에 따라 클릭이 안될 수도 있음)
        try:
            click_target = place_list[i].find_element(By.XPATH, "./ancestor::div[contains(@class, 'place_bluelink')]")
            click_target.click()
            time.sleep(2)
        except:
            print("place_bluelink 찾을 수 없음")
            time.sleep(3)
            driver.quit()
            exit()

        driver.switch_to.default_content()
        #entryIframe으로 이동(리뷰와 장소 상세정보가 있음)
        try:
            WebDriverWait(driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.ID,"entryIframe"))
            )
        except:
            print("entryIframe 찾을 수 없음")
            time.sleep(3)
            driver.quit()
            exit()
        #리뷰 버튼 클릭
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,'//span[text()="리뷰"]'))
            ).click()
            
        except:
            print("리뷰 버튼 찾을 수 없음")
            time.sleep(3)
            driver.quit()
            exit()

        try:
            driver.switch_to.default_content()
            driver.switch_to.frame("searchIframe")
        except:
            print("searchIframe 이동 실패")
            time.sleep(3)
            driver.quit()
            exit()

        time.sleep(2)
        driver.execute_script("window.scrollBy(0, window.innerHeight);")

        review_list = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='pui__vn15t2']/a"))
        )

        for idx, review in enumerate(review_list):
            review_text = review.text
            if review_text != '더보기':
                place_info[place_name]["review"].append(review_text)

result = json.dumps(place_info, ensure_ascii=False, indent=4)
print(result)