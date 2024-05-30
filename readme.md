## Slack Message Analyzer
This project is a Python-based Slack message analyzer. It fetches messages from a specified Slack channel within a given time range, writes the messages to a file, and generates a summary of the messages.

## Project Structure
### Key Files
- main.py: This is the main entry point of the application. It fetches messages from a Slack channel using the get_slack_messages function, writes the messages to output/ - messages.txt, generates a summary using the generate_summary function, and writes the summary to output/summary.txt.
- utils/get_slack_messages.py: This file contains the get_slack_messages function which fetches messages from a Slack channel.
- utils/summarize_slack_messages.py: This file contains the generate_summary function which generates a summary of the fetched messages.
- output/messages.txt: This file contains the fetched Slack messages.
- output/summary.txt: This file contains the summary of the fetched messages.
- prompts/post_summary.txt: This file contains a prompt for the summary format.

### How to Run
To run the application, execute the main.py file:

This will fetch messages from the specified Slack channel, write the messages to output/messages.txt, generate a summary, and write the summary to output/summary.txt.

### Note
Please ensure that you have the necessary permissions and tokens to access the Slack API.