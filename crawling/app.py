import time
import random 
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
driver = webdriver.Chrome()
driver.get("https://map.naver.com/v5") #get() 원하는 링크로 이동
time.sleep(random.uniform(2,5))

#검색창 요소 찾기
search_input = driver.find_element(By.CLASS_NAME, "input_search")
search_input.send_keys("괴정동 맛집")
search_input.send_keys(Keys.ENTER)

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
    print("에러 발생")
    driver.quit()
    exit()

place_info = {}

if place_list:
    for i in range(7):
        place_name = place_list[i].text.strip()
        place_info[place_name] = {"review": []}
        
        place_list[i].click()
        time.sleep(2)
        
        driver.switch_to.default_content()
        try:
            driver.switch_to.frame("searchIframe")
        except:
            print("에러")


input()