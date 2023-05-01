import os
import re

import dotenv
import openai
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound
import gradio as gr

# Load environment variables
dotenv.load_dotenv()
openai_key = os.getenv("OPENAI_KEY")
openai_organization = os.getenv("OPENAI_ORGANIZATION")

# OpenAI API configurations
openai.api_key = openai_key
openai.organization = openai_organization

def summarize_video(youtube_url, language_code, prompt):
    """Function to get and process the subtitles, and return the summaries."""

    # Extract video id from url
    video_id = re.findall(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', youtube_url)[0]

    print("Loading subtitles...")
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_transcript([language_code])
        subtitles = transcript.fetch()
    except NoTranscriptFound:
        print("Error: No subtitles found in the specified language.")
        return

    # Collect subtitles without timestamps
    text = ""
    for subtitle in subtitles:
        text += subtitle['text'] + " "

    print("Splitting text...")
    # Chunk the text around 1000 characters
    chunks = []
    start = 0
    while start < len(text):
        end = start + 1000
        if end < len(text):
            end = text.rfind(' ', start, end)
            if end == -1:  # If no space is found, cut at 1000 characters
                end = start + 1000
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
iface = gr.Interface(fn=summarize_video,
                     inputs=["text", "text", "text"],
                     outputs="text")

# Launch Gradio interface
iface.launch()
