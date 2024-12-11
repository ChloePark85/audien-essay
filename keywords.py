KEYWORDS = {
    "감정/심리": [
        "불안", "설렘", "외로움", "우울", "자존감", "소심함", "공허함", "위축감", "결핍", 
        "불면증", "완벽주의", "우유부단", "강박", "무기력", "번아웃", "새로운 시작", 
        "희망", "설레는 기대", "자책", "후회"
    ],
    "관계": [
        "썸", "짝사랑", "이별", "SNS", "읽씹", "친구관계", "가족갈등", "직장동료", 
        "선약취소", "약속", "모임", "술자리", "카톡", "인스타그램", "첫인상", "오해", 
        "관계단절", "화해", "재회", "새로운 인연"
    ],
    "일상/생활": [
        "출퇴근", "자취", "집콕", "배달음식", "야근", "주말", "데이트", "카페", "운동", 
        "다이어트", "취미", "공부", "여행", "독서", "영화", "음악", "산책", "쇼핑", 
        "집들이", "반려동물"
    ],
    "고민/걱정": [
        "취업", "이직", "스펙", "연봉", "결혼압박", "나이듦", "미래계획", "재테크", 
        "자기계발", "비교의식", "성형", "다이어트", "채무", "독립", "진로", 
        "업무스트레스", "면접", "경쟁", "실패", "목표상실"
    ],
    "장소/공간": [
        "원룸", "회사", "지하철", "동네카페", "한강공원", "대형마트", "동네골목", "옥상", 
        "공원", "서점", "영화관", "미용실", "편의점", "병원", "피트니스센터", "한적한 거리", 
        "번화가", "골목길", "기차역", "공항"
    ]
}

def get_random_keywords(num_keywords=5):
    """
    각 카테고리에서 랜덤하게 키워드를 선택합니다.
    기본적으로 총 5개의 키워드를 반환합니다.
    """
    import random
    
    selected = []
    categories = list(KEYWORDS.keys())
    
    # 최소한 각 카테고리에서 하나씩 선택
    for category in random.sample(categories, min(num_keywords, len(categories))):
        selected.append(random.choice(KEYWORDS[category]))
    
    # 필요한 만큼 추가 키워드 선택
    while len(selected) < num_keywords:
        category = random.choice(categories)
        keyword = random.choice(KEYWORDS[category])
        if keyword not in selected:
            selected.append(keyword)
    
    return selected