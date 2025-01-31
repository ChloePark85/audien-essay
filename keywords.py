# keywords.py
REALESTATE_TOPICS = {
   "계약실무": {
       "전월세": [
           {"situation": "계약서 작성", "desc": "계약서 체크포인트"},
           {"situation": "권리분석", "desc": "등기부등본 읽기"},
           {"situation": "물건확인", "desc": "현장답사 체크리스트"},
           {"situation": "가격협상", "desc": "시세 분석과 협상법"}
       ],
       "매매": [
           {"situation": "자금계획", "desc": "대출과 청약"},
           {"situation": "입지분석", "desc": "상권과 교통"},
           {"situation": "투자가치", "desc": "시세동향 분석"},
           {"situation": "세금계산", "desc": "취득세와 보유세"}
       ]
   },
   "실전노하우": {
       "준비단계": [
           {"situation": "자금준비", "desc": "저축과 대출"},
           {"situation": "정보수집", "desc": "매물 검증법"},
           {"situation": "시기선택", "desc": "시장 진입 시점"}
       ],
       "실행단계": [
           {"situation": "물건선정", "desc": "매물 비교분석"},
           {"situation": "협상전략", "desc": "가격 협상법"},
           {"situation": "계약진행", "desc": "계약 프로세스"}
       ]
   },
   "핵심요소": {
       "실무": ["법률검토", "자금설계", "시세분석", "권리관계", "계약절차"],
       "전략": ["가격협상", "입지분석", "투자전략", "리스크관리", "시장전망"],
       "실행": ["현장확인", "서류검토", "자금조달", "절세방안", "등기이전"]
   }
}

class TopicSelector:
   def __init__(self):
       self.used_combinations = set()
   
   def get_unused_topic(self):
       import random
       
       available_combinations = []
       for category, areas in REALESTATE_TOPICS.items():
           if category != "핵심요소":
               for area, topics in areas.items():
                   for topic in topics:
                       if topic["situation"] not in self.used_combinations:
                           practical = random.choice(REALESTATE_TOPICS["핵심요소"]["실무"])
                           strategy = random.choice(REALESTATE_TOPICS["핵심요소"]["전략"])
                           execution = random.choice(REALESTATE_TOPICS["핵심요소"]["실행"])
                           
                           available_combinations.append({
                               "category": category,
                               "area": area,
                               "situation": topic["situation"],
                               "desc": topic["desc"],
                               "practical": practical,
                               "strategy": strategy,
                               "execution": execution
                           })
       
       if not available_combinations:
           return None
       
       selected = random.choice(available_combinations)
       self.used_combinations.add(selected['situation'])
       return selected

selector = TopicSelector()

def get_topic():
   return selector.get_unused_topic()