import os
import time
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SLACK_API_TOKEN = os.getenv("SLACK_API_TOKEN")

def get_slack_messages(slack_channel_id, start_time_str, end_time_str):
    slack_messages = []
    
    current_date = datetime.strptime(start_time_str, '%m/%d/%Y')
    end_date = datetime.strptime(end_time_str, '%m/%d/%Y')

    while current_date <= end_date:
        current_timestamp = int(current_date.timestamp())
        url = f'https://slack.com/api/conversations.history?channel={slack_channel_id}&oldest={current_timestamp}&latest={current_timestamp + 24 * 60 * 60}'

        headers = {
            'Authorization': f'Bearer {SLACK_API_TOKEN}',
        }

        retry_count = 0
        max_retries = 5
        backoff_time = 3

        while retry_count < max_retries:
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                break
            except requests.RequestException as e:
                retry_count += 1
                if retry_count >= max_retries:
                    raise Exception('Exceeded maximum retry attempts') from e
                time.sleep(backoff_time)
                backoff_time *= 2

        data = response.json()
        messages = data.get('messages', [])

        if not messages:
            current_date += timedelta(days=1)
            continue

        for message in messages:
            try:
                if message.get('type') == 'message' or message.get('subtype') == 'bot_message':
                    ts = float(message['ts'])
                    date_object = datetime.fromtimestamp(ts)
                    date = date_object.strftime("%m/%d/%Y")
                    text = message.get('text', '')

                    permalink_url = f'https://slack.com/api/chat.getPermalink?channel={slack_channel_id}&message_ts={ts}'
                    permalink_response = requests.get(permalink_url, headers=headers)
                    permalink_data = permalink_response.json()
                    permalink = permalink_data.get('permalink', '')
                    attachments = message.get('attachments', [])

                    attachment_urls = '\n'.join(att.get('title_link', att.get('text', '')) for att in attachments if att.get('title_link') or att.get('text'))
                    source_footers = ''.join(att.get('footer', '') for att in attachments)

                    slack_messages.append([date, text, source_footers, permalink, attachment_urls])

                    # Check if the message has more threaded replies
                    if message.get('thread_ts'):
                        thread_replies = get_thread_replies(slack_channel_id, message['thread_ts'])
                        slack_messages.extend(thread_replies)
            except Exception as e:
                continue

        current_date += timedelta(days=1)

    return slack_messages

def get_thread_replies(slack_channel_id, thread_ts):
    url = f'https://slack.com/api/conversations.replies?channel={slack_channel_id}&ts={thread_ts}'
    headers = {
        'Authorization': f'Bearer {SLACK_API_TOKEN}',
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    data = response.json()
    messages = data.get('messages', [])

    thread_replies = []
    for message in messages:
        ts = float(message['ts'])
        date_object = datetime.fromtimestamp(ts)
        date = date_object.strftime("%m/%d/%Y")
        text = message.get('text', '')

        permalink_url = f'https://slack.com/api/chat.getPermalink?channel={slack_channel_id}&message_ts={ts}'
        permalink_response = requests.get(permalink_url, headers=headers)
        permalink_data = permalink_response.json()
        permalink = permalink_data.get('permalink', '')
        attachments = message.get('attachments', [])

        attachment_urls = '\n'.join(att.get('title_link', att.get('text', '')) for att in attachments if att.get('title_link') or att.get('text'))
        source_footers = ''.join(att.get('footer', '') for att in attachments)

        thread_replies.append([date, text, source_footers, permalink, attachment_urls])

    return thread_replies
