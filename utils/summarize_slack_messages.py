from openai import OpenAI
client = OpenAI()

def get_gpt_response(prompt):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message

def generate_summary(messages):
    summary_prompt = 'prompts/post_summary.txt'
    prompt = open(summary_prompt).read() + "\n" + messages
    summary = get_gpt_response(prompt) # Need to add new get_gpt_response function
    
    return summary

def summarize_slack_messages(messages):    
    post_summary = '/prompts/post_summary.txt'
    finalSummaryPrompt = post_summary + "\n" + combinedPreSummaries
    finalSummary = get_gpt_response(finalSummaryPrompt) # Need to add new get_gpt_response function
    return finalSummary