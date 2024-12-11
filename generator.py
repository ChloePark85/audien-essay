import os
import anthropic
from dotenv import load_dotenv
import random

load_dotenv()

class StoryGenerator:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.series_count = 0

    def generate_story(self, keywords):
        self.series_count += 1
        selected_keywords = random.sample(keywords, random.randint(2, 3))
        
        prompt = f"""
        당신은 27살 여성 작가 '서하영'입니다. '서울, 나의 외로움이 자라는 곳' 연작 시리즈를 연재하고 있습니다.
        
        다음 키워드 중에서 자연스럽게 사용할 수 있는 것을 선택하여 에세이를 작성해주세요: {', '.join(selected_keywords)}

        필수 포함 요소:
        1. 구체적인 장면 묘사
        - 계절감과 날씨
        - 시간대와 장소의 디테일한 묘사
        - 오감을 활용한 생생한 표현
        - 주변 사람들의 모습과 소리
        
        2. 다양한 대화 형식
        - 현재 진행되는 생생한 대화 (최소 5개 이상의 대화)
        - 과거 회상 속 대화
        - 카톡이나 메시지 내용
        - 내면의 독백
        
        3. 감정과 생각의 깊이
        - 겉으로 드러나는 감정
        - 속으로 감추고 있는 본심
        - 과거와 현재를 오가는 생각의 흐름
        - 나를 돌아보는 성찰
        
        4. 분량과 구성
        - 최소 4000자 이상
        - 3-4개의 주요 장면으로 구성
        - 각 장면마다 구체적인 대화 포함
        - 시간의 흐름에 따른 자연스러운 전개
        
        글의 예시적 구성:
        - 도입: 현재의 구체적인 장면과 생생한 대화
        - 전개: 과거 회상과 그 속의 대화들
        - 절정: 갈등이나 깨달음의 순간
        - 마무리: 현재로 돌아와 새로운 시각으로 바라보는 마무리
        
        작가의 시선으로 쓰되, 독자가 현장에 함께 있는 것처럼 생생하게 써주세요.
        대화는 실제 20대들의 대화처럼 자연스럽게 표현해주세요.

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
            return response.content[0].text, selected_keywords
        except Exception as e:
            print(f"Error generating story: {e}")
            return None, None