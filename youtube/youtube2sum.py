import os
import re
import argparse

import dotenv
import openai
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound

# Load environment variables
dotenv.load_dotenv()
openai_key = os.getenv("OPENAI_KEY")
openai_organization = os.getenv("OPENAI_ORGANIZATION")

# OpenAI API configurations
openai.api_key = openai_key
openai.organization = openai_organization

def main():
    """Main function to get and process the subtitles, and save the summaries."""
    # Create argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("youtube_url", help="YouTube video URL.")
    parser.add_argument("language_code", help="Language code for the subtitles.")
    args = parser.parse_args()

    # Extract video id from url
    video_id = re.findall(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', args.youtube_url)[0]

    print("字幕を読み込み中\n")
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_transcript([args.language_code])
        subtitles = transcript.fetch()
    except NoTranscriptFound:
        print("エラー：指定した言語の字幕が見つかりませんでした。")
        return

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
                prompt="議論の概要と議論のポイントをまとめて:summary so far["+summary+"] additional text: "+chunk,
                temperature=0.3,
                max_tokens=4000
            )
            summary = response.choices[0].text.strip()

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt="日本語で議論の概要と議論のポイントをmarkdown方式でまとめて:"+summary,
            temperature=0.3,
            max_tokens=4000
        )

        summary = response.choices[0].text.strip()
        out_file.write(summary + '\n\n')

if __name__ == "__main__":
    main()
