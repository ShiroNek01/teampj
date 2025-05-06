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

search_place = input("검색어 입력 : ")

# options.add_argument("--headless") #백그라운드 실행 
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
driver = webdriver.Chrome(options=options)

#네이버 지도 열기
driver.get("https://map.naver.com/v5") #get() 원하는 링크로 이동
time.sleep(random.uniform(2,4))

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

place_info = {}
index = 0

while True:
    #검색 결과 요소 가져오기
    try:
        place_list = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[contains(@class, 'TYaxT') or contains(@class, 'YwYLL')]"))
        )
        print(f"{len(place_list)}")
    except:
        print("요소 찾을 수 없음")
        driver.quit()
        exit()

    end_index = min(index + 3, len(place_list))

    if place_list:
        for i in range(index, end_index):
            place_name = place_list[i].text.strip()

            if place_name in place_info:
                continue

            place_info[place_name] = {
                "review": [], #리뷰
                "images": [], #이미지
                "location":"", #위치
                "operate":"", #운영시간
                "contact":"", #연락처
                "website":"" #홈페이지
                }

            #클릭
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
                print('_')
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

            max_review = 90
            collected = 0
            scroll_count = 0
            max_scroll = 10

            while True:
                #리뷰 스크롤 내리기
                driver.execute_script("window.scrollBy(0, window.innerHeight);")
                time.sleep(1)

                #리뷰 수집
                review_list = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//div[@class='pui__vn15t2']/a"))
                )

                for review in review_list:
                    review_text = review.text
                    if review_text not in ('더보기', '') and review_text not in place_info[place_name]["review"]:
                        place_info[place_name]["review"].append(review_text)
                        collected += 1
                    if collected >= max_review:
                        break
                if collected >= max_review:
                    break
                
                #더보기 클릭
                try:
                    more_bt = driver.find_element(By.XPATH, "//a[@class='fvwqf']")
                    more_bt.click()
                    time.sleep(1)
                except:
                    pass
                if len(review_list) <= collected or scroll_count >= max_scroll:
                    break
                scroll_count += 1

            img_list = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//a[@class='place_thumb']/img"))
            )

            #이미지 수집
            for img in img_list[:5]:
                img_url = img.get_attribute("src")  # 이미지 URL 가져오기
                place_info[place_name]["images"].append(img_url) 

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
        with open("result.json", "w", encoding="utf-8") as f:
            json.dump(place_info, f, ensure_ascii=False, indent=4)

        index = end_index
        print('=============================')
        more_info = input("continue? (y/n) : ")
        if more_info.lower() == 'n':
            print('종료\n=============================')
            break
        elif more_info.lower() != 'y':
            print('재입력 : ')
            continue
        else:
            print('=============================')