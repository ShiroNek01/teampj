# 형태소 분석기를 쓰지 않고 문장을 단어 단위로 나눌 수 있게하는 모듈
from soynlp.tokenizer import RegexTokenizer

#json 데이터 파일 읽기 용 모듈
import json

#테마별 출현 횟수를 세기 위해 필요함
from collections import Counter

#테마를 분류하기 위한 키워드
#각 테마는 장소의 특징을 나타내며, 해당하는 키워드들을 리스트로 묶어놓음
#이후 crawler.py 에서 수집한 리뷰 데이터에서 키워드의 출현 빈도에 따라 테마를 분류함
keyword = {
    "힐링": ['자연', '산책', '풍경', '경치', '뷰', '공원', '야경', '조용', '편안', '휴식', '쉼', '명상', '여유', '숲'],
    "여름": ['바다', '해수욕', '물놀이', '해변', '모래사장', '계곡', '수영', '파라솔', '서핑'],
    "맛집": ['맛있', '잘먹', '맛집', '요리', '식사', '음식', '한끼', '먹방', '풍미', '입맛', '요리법'],
    "모임": ['단체', '모임', '회식', '친구', '모여', '단체석', '예약', '단체룸'],
    "데이트": ['커플', '분위기', '로맨틱', '산책', '전망', '야경', '데이트', '조명', '감성'],
    "가족": ['아이', '어린이', '부모', '어르신', '놀이공원', '체험', '가족', '유모차', '휴양'],
    "액티비티": ['레저', '체험', '스릴', '놀이', '클라이밍', '집라인', '서바이벌', '짚라인', '승마', 'ATV'],
    "문화예술": ['미술관', '박물관', '전시', '예술', '공연', '전시회', '문화', '관람'],
    "사진": ['포토존', '인생샷', '감성샷', '사진', '찍기좋', '뷰맛집', '카메라'],
    "야경": ['야경', '불빛', '야시장', '조명', '전망대', '야간', '밤', '빛'],
}

#soynlp에서 제공하는 정규식 기반 토크나이저 초기화
#기본 설정으로 한글 문장을 공백 기분이 아닌 정규식 기반으로 토큰화
tokenizer = RegexTokenizer()


#테마 추출 함수
def extract(reviews):
    theme_count = Counter()     #테마별 키워드 출현 횟수 저장

    for review in reviews:
        #리뷰들을 토큰화하여 리스트로 반환
        tokens = tokenizer.tokenize(review, flatten=True)
        
        #그리고 각 테마에 대해 해당 키워드가 토큰 안에 존재하는지 확인
        for theme, keywords in keyword.items():
            #tokens 내에 keywords 중 하나라도 포함되면 count 증가
            if any(kw in token for kw in keywords for token in tokens):
                theme_count[theme] += 1

    #출현 빈도 기준으로 내림차순 정렬하여 상위 3개 테마 추출함
    return [theme for theme, _ in theme_count.most_common(3)]

#json 파일 result.json 불러옴
with open('result.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

#장소별 리뷰에 대해 테마 추출 및 데이터에 저장
#themes라는 새 키를 추가하여 테마 분석 결과를 저장함
for place_name, info in data.items():
    #해당 장소의 리뷰 리스트를 추출하고 테마 분석
    themes = extract(info.get("review", []))
    #themes 필드로 결과 저장
    data[place_name]["themes"] = themes

#json 형식으로 출력
print(json.dumps(data, ensure_ascii=False, indent=4))