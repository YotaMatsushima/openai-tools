import os
import re
import dotenv
import openai
import praw
import gradio as gr

# Load environment variables
dotenv.load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
user_agent = os.getenv("USER_AGENT")
openai_key = os.getenv("OPENAI_KEY")
openai_organization = os.getenv("OPENAI_ORGANIZATION")

# OpenAI API configurations
openai.api_key = openai_key
openai.organization = openai_organization

def remove_special_characters(text):
    """Function to remove emojis and special characters."""
    # Remove emojis
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)

    # Remove periods and commas
    text = text.replace('.', '').replace(',', '')

    return text

def summarize_thread(thread_id, prompt):
    """Function to get and process the comments, and return the summaries."""
    # Create PRAW instance
    reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

    # Get the comments of the thread
    submission = reddit.submission(id=thread_id)
    submission.comment_sort = 'best'  # Sort comments by best
    submission.comment_limit = 50  # Limit the number of comments to 50

    # Collect comments and count the total number of characters
    text = ""
    for comment in submission.comments.list():
        if isinstance(comment, praw.models.Comment):
            cleaned_comment = remove_special_characters(comment.body)
            text += f"{comment.author}: {cleaned_comment}\n\n"

    # Chunk the text around 1500 characters
    chunks = []
    start = 0
    while start < len(text):
        end = start + 1500
        if end < len(text):
            end = text.rfind('\n', start, end)
            if end == -1:  # If no newline is found, cut at 1500 characters
                end = start + 1500
        chunks.append(text[start:end])
        start = end

    summaries = []
    # Generate a summary for each chunk
    for chunk in chunks:
        messages = [
            {"role": "system", "content": "You are a helpful assistant that summarizes text."},
            {"role": "user", "content": prompt + ": " + chunk}
        ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )
        summary = response['choices'][0]['message']['content']
        summaries.append(summary)

    return "\n\n".join(summaries)


# Define Gradio interface
iface = gr.Interface(fn=summarize_thread,
                     inputs=["text", "text"],
                     outputs="text")

# Launch Gradio interface
iface.launch()
