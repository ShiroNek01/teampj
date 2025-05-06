from soynlp.tokenizer import RegexTokenizer
import json
from collections import Counter

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

tokenizer = RegexTokenizer()

def extract(reviews):
    theme_count = Counter()

    for review in reviews:
        tokens = tokenizer.tokenize(review, flatten=True)
        for theme, keywords in keyword.items():
            if any(kw in token for kw in keywords for token in tokens):
                theme_count[theme] += 1

    return [theme for theme, _ in theme_count.most_common(3)]

with open('result.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for place_name, info in data.items():
    themes = extract(info.get("review", []))
    data[place_name]["themes"] = themes

print(json.dumps(data, ensure_ascii=False, indent=4))