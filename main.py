from utils.get_slack_messages import get_slack_messages
from utils.summarize_slack_messages import generate_summary
from datetime import datetime, timedelta

def main():
    slack_channel_id = 'C02AGSGPHNG'
    start_time_str = '5/20/2024'
    end_time_str = '5/31/2024'
    messages_output_file = 'output/messages.txt'
    summary_output_file = 'output/summary.txt'
    message_str = ""

    messages = get_slack_messages(slack_channel_id, start_time_str, end_time_str)    
    
    with open(messages_output_file, 'w') as file:
        for message in messages:
            message_str += " ".join(message) + '\n'
        file.write(message_str)
            
    summary = generate_summary(message_str)
    
    with open(summary_output_file, 'w') as file:
        file.write(summary.content)

if __name__ == "__main__":
    main()
