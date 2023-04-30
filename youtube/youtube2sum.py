import os
import re

import dotenv
import openai
from youtube_transcript_api import YouTubeTranscriptApi

# Load environment variables
dotenv.load_dotenv()
openai_key = os.getenv("OPENAI_KEY")
openai_organization = os.getenv("OPENAI_ORGANIZATION")

# OpenAI API configurations
openai.api_key = openai_key
openai.organization = openai_organization

def main():
    """Main function to get and process the subtitles, and save the summaries."""
    # Specify the Youtube video URL
    youtube_url = input("Youtube URL:")

    # Extract video id from url
    video_id = re.findall(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', youtube_url)[0]

    print("字幕を読み込み中\n")

    # Get the subtitles of the video
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    transcript = transcript_list.find_transcript(['ja'])
    subtitles = transcript.fetch()

    # Collect subtitles without timestamps
    text = ""
    for subtitle in subtitles:
        text += subtitle['text'] + " "

    print("テキストを分割中\n")
    # Chunk the text around 1500 characters
    chunks = []
    start = 0
    while start < len(text):
        end = start + 500
        if end < len(text):
            end = text.rfind(' ', start, end)
            if end == -1:  # If no space is found, cut at 1500 characters
                end = start + 500
        chunks.append(text[start:end])
        start = end

    summary=''
    # Generate a summary for each chunk
    with open(f'outputs/summary_{video_id}.md', 'w') as out_file:
        for chunk in chunks:
            print(chunk)
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt="日本語で議論の概要とポイントをmarkdown方式でまとめる:summary so far["+summary+"] 1additional text: "+chunk,
                temperature=0.3,
                max_tokens=4000
            )
            summary = response.choices[0].text.strip()

        out_file.write(summary + '\n\n')

if __name__ == "__main__":
    main()
