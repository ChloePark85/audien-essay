from flask import Flask, request, jsonify
import threading
import re
from slack_uploader import SlackUploader
import json

app = Flask(__name__)

@app.route('/slack/events', methods=['POST'])
def handle_slack_event():
    content_type = request.headers.get('Content-Type', '')
    print(f"\n[DEBUG] Received request with Content-Type: {content_type}")

    try:
        if content_type == 'application/json':
            data = request.json
            print(f"[DEBUG] JSON data received: {json.dumps(data, indent=2)}")
            
            # 메시지 이벤트 처리
            if data.get('type') == 'event_callback' and data['event']['type'] == 'message':
                print("[DEBUG] Message event detected")
                event = data['event']
                print(f"[DEBUG] Event data: {json.dumps(event, indent=2)}")
                
                # 봇 메시지 무시
                if event.get('bot_id'):
                    print("[DEBUG] Ignoring bot message")
                    return jsonify({'status': 'ok'})
                
                if 'thread_ts' in event and '수정본:' in event.get('text', ''):
                    print("[DEBUG] Revision message detected")
                    text_content = event['text'].replace('수정본:', '').strip()
                    thread_ts = event['thread_ts']
                    
                    print(f"[DEBUG] Revision text: {text_content[:100]}...")
                    print(f"[DEBUG] Thread ts: {thread_ts}")
                    
                    uploader = SlackUploader()
                    threading.Thread(
                        target=uploader.generate_content,
                        args=(text_content, thread_ts)
                    ).start()
                    print("[DEBUG] Started revision processing thread")
                
                elif 'thread_ts' in event and '배경음악:' in event.get('text', ''):
                    print("[DEBUG] Background music message detected")
                    uploader = SlackUploader()
                    uploader.handle_message(event)
        elif content_type == 'application/x-www-form-urlencoded':
            form_data = request.form
            print(f"[DEBUG] Form data received: {form_data}")
            
            if 'payload' in form_data:
                data = json.loads(form_data['payload'])
                print(f"[DEBUG] Parsed payload: {json.dumps(data, indent=2)}")
                
                # 버튼 클릭 이벤트 처리
                if data.get('type') == 'block_actions':
                    print("[DEBUG] Block actions detected")
                    action = data['actions'][0]
                    print(f"[DEBUG] Action: {action}")
                    
                    if action['action_id'] == 'generate_content':
                        print("[DEBUG] Generate content button clicked")
                        message = data['message']
                        text_content = message['blocks'][0]['text']['text']
                        thread_ts = message['ts']
                        
                        print(f"[DEBUG] Text content length: {len(text_content)}")
                        print(f"[DEBUG] Thread ts: {thread_ts}")
                        
                        uploader = SlackUploader()
                        print("[DEBUG] Created SlackUploader instance")
                        
                        threading.Thread(
                            target=uploader.generate_content,
                            args=(text_content, thread_ts)
                        ).start()
                        print("[DEBUG] Started content generation thread")
                        
                        return jsonify({'response_type': 'in_channel'})
            else:
                data = form_data.to_dict()
                print(f"[DEBUG] Converted form data: {data}")
        else:
            print(f"[DEBUG] Unsupported Content-Type: {content_type}")
            return jsonify({'error': 'Unsupported Media Type'}), 415

        # URL 검증 처리
        if data.get('type') == 'url_verification':
            print("[DEBUG] URL verification request")
            return jsonify({'challenge': data.get('challenge')})
        
        return jsonify({'status': 'ok'})
    
    except Exception as e:
        print(f"[DEBUG] Error in handle_slack_event: {str(e)}")
        import traceback
        print("[DEBUG] Full traceback:")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

def handle_button_click(data):
    """결과물 생성 버튼 클릭 처리"""
    print("Processing button click")  # 디버깅
    try:
        message = data['message']
        text_content = message['blocks'][0]['text']['text']
        thread_ts = message['ts']
        print(f"Extracted text content length: {len(text_content)}, thread_ts: {thread_ts}")  # 디버깅
        
        uploader = SlackUploader()
        threading.Thread(
            target=uploader.generate_content,
            args=(text_content, thread_ts)
        ).start()
    except Exception as e:
        print(f"Error in handle_button_click: {e}")

def handle_revision(event):
    """수정본 메시지 처리"""
    print("Processing revision")  # 디버깅
    try:
        text_content = event['text'].replace('수정본:', '').strip()
        thread_ts = event['thread_ts']
        print(f"Extracted revision text length: {len(text_content)}, thread_ts: {thread_ts}")  # 디버깅
        
        uploader = SlackUploader()
        threading.Thread(
            target=uploader.generate_content,
            args=(text_content, thread_ts)
        ).start()
    except Exception as e:
        print(f"Error in handle_revision: {e}")

if __name__ == '__main__':
    print("Starting Flask server on port 3000...")
    app.run(port=3000, debug=True)