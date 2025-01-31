# generator.py
import os
import anthropic
from dotenv import load_dotenv
from keywords import get_topic

load_dotenv()

class StoryGenerator:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.series_count = 0

    def generate_story(self):
        self.series_count += 1
        topic = get_topic()
        
        if not topic:
            return None, None
        
        prompt = f"""
부동산 전문가이자 파이낸셜 플래너로서 '부동산 첫 걸음: 전월세 계약부터 내 집 마련까지'를 작성한다. 실용적인 부동산 가이드로 각 에피소드별로 4000자를 작성한다.
글 내용에 소제목을 넣지마라. 
글쓰기 원칙:
1. 내용과 구성:
- 실용적인 정보와 팁 (60%)
- 구체적인 사례와 에피소드 (30%)
- 전문가 조언 (10%)
- 자연스러운 흐름으로 구성

2. 사례/에피소드 포함:
- 실제 계약/매매 사례
- 구체적인 금액과 조건
- 실패와 성공 사례
- 주의해야 할 함정
- 실전 협상 팁

3. 문체:
- 다양한 어투 사용: ~다, ~요, ~죠, ~까요?, ~죠?, ~곤 한다, ~기 때문이다, ~곤 하죠, ~이므로, ~요
- 불필요한 주어 반복 금지
- 전문용어는 쉽게 설명
- 구체적이고 명확한 표현

4. 실용성 강화:
- 구체적인 수치와 법적 근거
- 실제 계약서 작성 팁
- 자금 계획 수립 방법
- 체크리스트와 주의사항

5. 금지사항:
- 검증되지 않은 정보
- 불확실한 시장 전망
- 투기 조장 내용
- 번호 매기기나 나열식 구성

이번 글의 주제:
분야: {topic['situation']}
특징: {topic['desc']}
핵심요소:
- 실무: {topic['practical']}
- 전략: {topic['strategy']}
- 실행: {topic['execution']}

글의 구성 방향:
- 도입: 상황 설정과 문제 제시
- 전개: 구체적인 해결 방법과 팁
- 사례: 실제 경험과 교훈
- 마무리: 실용적인 조언과 체크포인트
"""

        try:
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4000,
                messages=[{
                    "role": "user", 
                    "content": prompt
                }]
            )
            return response.content[0].text, topic
        except Exception as e:
            print(f"Error generating content: {e}")
            return None, None