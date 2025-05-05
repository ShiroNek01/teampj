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

#백그라운드 실행
# options.add_argument("--headless")  
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
driver = webdriver.Chrome(options=options)

#네이버 지도 열기
driver.get("https://map.naver.com/v5") #get() 원하는 링크로 이동
time.sleep(random.uniform(2,5))

search_place = input("\n==========================\n검색어 입력 : \n==========================\n")

#검색창 요소 찾기
search_input = driver.find_element(By.CLASS_NAME, "input_search")
search_input.send_keys(search_place)
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
        place_info[place_name] = {
            "review": [], #리뷰
            "location":"", #위치
            "operate":"", #운영시간
            "contact":"", #연락처
            "website":"" #홈페이지
            }

        #부모 요소를 클릭(자식 요소를 클릭할 경우 텍스트에 따라 클릭이 안될 수도 있기에)
        try:
            click_target = place_list[i].find_element(By.XPATH, "./ancestor::div[contains(@class, 'place_bluelink')]")
            click_target.click()
            time.sleep(2)
        except:
            print("place_bluelink 찾을 수 없음")
            time.sleep(3)
            driver.quit()
            exit()
            
        #entryIframe으로 이동(리뷰와 장소 상세정보가 있음)
        driver.switch_to.default_content()
        try:
            WebDriverWait(driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.ID,"entryIframe"))
            )
        except:
            print("entryIframe 찾을 수 없음")
            time.sleep(3)
            driver.quit()
            exit()

        #기타 상세 정보 수집
        #장소 위치
        try:
            location = driver.find_element(By.CLASS_NAME, "LDgIH").text
            place_info[place_name]["location"] = location
            print('_', end='')
        except:
            print('/', end='')
            place_info[place_name]["location"] = "--"

        #운영 정보
        try:
            operate = driver.find_element(By.CLASS_NAME, "A_cdD").text
            place_info[place_name]["operate"] = operate
            print('_', end='')
        except:
            print('/', end='')
            place_info[place_name]["operate"] = "--"

        #연락처
        try:
            contact = driver.find_element(By.CLASS_NAME, "xlx7Q").text
            place_info[place_name]["contact"] = contact
            print('_', end='')
        except:
            print('/', end='')
            place_info[place_name]["contact"] = "--"

        #웹사이트 링크
        try:
            website = driver.find_element(By.CLASS_NAME, "CHmqa").text
            place_info[place_name]["website"] = website
            print('_', end='')
        except:
            print('/\t')
            place_info[place_name]["website"] = "--"

        time.sleep(2)
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

        #리뷰 스크롤 내리기
        driver.execute_script("window.scrollBy(0, window.innerHeight);")

        #리뷰 수집
        review_list = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='pui__vn15t2']/a"))
        )

        for idx, review in enumerate(review_list):
            review_text = review.text
            if review_text != '더보기':
                place_info[place_name]["review"].append(review_text)

        #seacrhIframe으로 이동 (아직 entryIframe에 있기 때문)
        try:
            driver.switch_to.default_content()
            driver.switch_to.frame("searchIframe")
        except:
            print("searchIframe 이동 실패")
            time.sleep(3)
            driver.quit()
            exit()

result = json.dumps(place_info, ensure_ascii=False, indent=4)
print(result)

