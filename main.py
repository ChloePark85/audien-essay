from keywords import get_random_keywords
from generator import StoryGenerator
from slack_uploader import SlackUploader
import time
from datetime import datetime

def main():
    # 인스턴스 생성
    generator = StoryGenerator()
    uploader = SlackUploader()
    
    # 5개의 에피소드 생성
    for episode in range(1, 6):
        try:
            print(f"\nGenerating episode {episode}/5...")
            
            # 랜덤 키워드 선택
            keywords = get_random_keywords()
            print(f"Selected initial keywords: {keywords}")
            
            # 현재 날짜
            current_date = datetime.now().strftime("%Y년 %m월 %d일")
            
            # 이야기 생성
            story, used_keywords = generator.generate_story(keywords)
            
            if story and used_keywords:
                print(f"Actually used keywords: {used_keywords}")
                
                # 슬랙에 업로드
                response = uploader.upload_story(story, used_keywords, current_date)
                if response:
                    print(f"Successfully posted episode {episode}/5 to Slack!")
                    print(f"Used keywords: {used_keywords}")
                else:
                    print(f"Failed to post episode {episode}")
            
            # 마지막 에피소드가 아니면 1분 대기
            if episode < 5:
                print("Waiting 1 minute before next episode...")
                time.sleep(60)
            
        except Exception as e:
            print(f"Error in episode {episode}: {e}")
            time.sleep(30)  # 에러 발생시 30초 대기 후 다음 에피소드 시도
    
    print("\nAll 5 episodes have been generated and posted. Program complete.")

if __name__ == "__main__":
    main()