# main.py
import os
from pathlib import Path
from generator import StoryGenerator
from slack_uploader import SlackUploader
import time
from datetime import datetime

def main():
    print("=== 부동산 첫걸음 가이드 생성기 시작 ===")
    print(f"시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    BASE_DIR = Path(__file__).resolve().parent
    STORIES_DIR = BASE_DIR / 'stories'
    
    print(f"\n1. 환경 설정 확인")
    print(f"- 작업 디렉토리: {BASE_DIR}")
    print(f"- 저장 디렉토리: {STORIES_DIR}")
    
    anthropic_key = os.getenv('ANTHROPIC_API_KEY')
    slack_token = os.getenv('SLACK_BOT_TOKEN')
    eleven_labs_key = os.getenv('ELEVENLABS_API_KEY')
    
    print("\n2. API 키 확인")
    print(f"- Anthropic API 키: {'설정됨' if anthropic_key else '미설정'}")
    print(f"- Slack Bot 토큰: {'설정됨' if slack_token else '미설정'}")
    print(f"- ElevenLabs API 키: {'설정됨' if eleven_labs_key else '미설정'}")
    
    if not all([anthropic_key, slack_token, eleven_labs_key]):
        print("\n⚠️ 오류: 필요한 API 키가 모두 설정되지 않았습니다.")
        print("다음 환경변수를 확인해주세요:")
        print("- ANTHROPIC_API_KEY")
        print("- SLACK_BOT_TOKEN")
        print("- ELEVENLABS_API_KEY")
        return
    
    print("\n3. 초기화 시작")
    try:
        print("- StoryGenerator 초기화 중...")
        generator = StoryGenerator()
        print("- SlackUploader 초기화 중...")
        uploader = SlackUploader()
        print("✓ 초기화 완료")
    except Exception as e:
        print(f"\n⚠️ 오류: 초기화 중 문제가 발생했습니다: {str(e)}")
        return
    
    print("\n4. 디렉토리 설정")
    STORIES_DIR.mkdir(exist_ok=True)
    print(f"- 스토리 저장 위치: {STORIES_DIR}")
    
    current_date = datetime.now().strftime("%Y%m%d_%H%M")
    series_folder = STORIES_DIR / f"부동산첫걸음_{current_date}"
    series_folder.mkdir(exist_ok=True)
    print(f"- 시리즈 폴더 생성: {series_folder}")
    
    episode = 1
    while True:
        try:
            print(f"\n=== 챕터 {episode} 생성 시작 ===")
            print("1. 주제 선정 및 내용 생성 중...")
            
            content, topic = generator.generate_story()
            
            if not content or not topic:
                print("\n⚠️ 더 이상 사용 가능한 주제가 없습니다.")
                print("모든 챕터가 완성되었습니다.")
                break
            
            print(f"✓ 주제 선정 완료: {topic['situation']}")
            print(f"- 분야: {topic.get('area', '미지정')}")
            print(f"- 설명: {topic.get('desc', '미지정')}")
            print(f"- 생성된 내용 길이: {len(content)} 자")
            
            current_date = datetime.now().strftime("%Y년 %m월 %d일")
            
            filename = series_folder / f"chapter_{episode}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"{topic['situation']}.\n")
                f.write(content)
                
            print(f"✓ 파일 저장 완료: {filename}")
            
            response = uploader.upload_story(content, topic, current_date)
            if response:
                print(f"✓ Slack 업로드 완료: 챕터 {episode}")
            else:
                print(f"⚠️ Slack 업로드 실패: 챕터 {episode}")
            
            if episode >= 12:
                print("\n✓ 시리즈가 모두 완성되었습니다.")
                break
            
            episode += 1
            print("\n다음 챕터 생성까지 10초 대기...")
            time.sleep(10)
            
        except Exception as e:
            print(f"⚠️ 에러 발생: 챕터 {episode}")
            print(f"에러 내용: {str(e)}")
            time.sleep(30)
    
    print("\n프로그램이 종료되었습니다.")

if __name__ == "__main__":
    main()