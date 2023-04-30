import os
import re

import dotenv
import openai
import praw

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

def main():
    """Main function to get and process the comments, and save the summaries."""
    # Create PRAW instance
    reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

    # Specify the thread ID
    thread_id = input("ThreadID:")
    print("Starting to load comments\n")

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

    print("Starting to chunk text\n")
    # Chunk the text around 1500 characters
    chunks = []
    start = 0
    while start < len(text):
        end = start + 1500
        if end < len(text):
            end = text.rfind('\n', start, end)
            if end == -1:  # If no newline is found, cut at 1000 characters
                end = start + 1500
        chunks.append(text[start:end])
        start = end

    summary=''
    # Generate a summary for each chunk
    with open(f'outputs/summary_{thread_id}.md', 'w') as out_file:
        for chunk in chunks:
            print(chunk)
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt="日本語で議論の概要とポイントをmarkdown方式でまとめる:summary so far["+summary+"] 1additional text: "+chunk,
                temperature=0.3,
                max_tokens=2500
            )
            summary = response.choices[0].text.strip()
            # Append the summary of the chunk to the file
            
        out_file.write(summary + '\n\n')

        # Add a final summary of the entire text to the file
       # response = openai.Completion.create(
       #     engine="text-davinci-003",
       #     prompt="overview 5Point for japanease:" + context,
       #     temperature=0.3,
       #     max_tokens=3500
       # )
       # total_summary = response.choices[0].text.strip()
       # out_file.write('\nOverView 5Point for Japanease:\n' + total_summary + '\n')

if __name__ == "__main__":
    main()

