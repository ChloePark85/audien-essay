import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class SlackUploader:
    def __init__(self):
        self.client = WebClient(token=os.getenv('SLACK_BOT_TOKEN'))
        self.channel = os.getenv('SLACK_CHANNEL')

    def upload_story(self, story, keywords, current_date):
        """
        생성된 이야기와 실제 사용된 키워드를 슬랙에 업로드합니다.
        """
        try:
            header = (
                f"*{current_date} 오늘의 에세이*\n"
                f"*사용된 키워드*: {', '.join(keywords)}\n"
                f"-------------------\n\n"
            )
            
            max_length = 3000
            story_chunks = [story[i:i + max_length] 
                          for i in range(0, len(story), max_length)]
            
            first_message = header + story_chunks[0]
            response = self.client.chat_postMessage(
                channel=self.channel,
                text=first_message,
                parse="mrkdwn"
            )
            
            for chunk in story_chunks[1:]:
                self.client.chat_postMessage(
                    channel=self.channel,
                    text=chunk,
                    thread_ts=response['ts'],
                    parse="mrkdwn"
                )
            
            return response
            
        except SlackApiError as e:
            print(f"Error uploading to Slack: {e}")
            return None