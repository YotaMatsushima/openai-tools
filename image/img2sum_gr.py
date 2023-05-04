import os
from dotenv import load_dotenv
import gradio as gr
from google.cloud import vision
import openai
import cv2
import numpy as np

# Load environment variables
load_dotenv()
google_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
openai_key = os.getenv("OPENAI_KEY")
openai_organization = os.getenv("OPENAI_ORGANIZATION")

# Google Cloud Vision API configurations
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_credentials

# OpenAI API configurations
openai.api_key = openai_key
openai.organization = openai_organization

def analyze_and_summarize(image):
    # Initialize a Vision API client
    client = vision.ImageAnnotatorClient()

    # Convert the image from a numpy array to bytes
    is_success, im_buf_arr = cv2.imencode(".jpg", image)
    byte_im = im_buf_arr.tobytes()

    vision_image = vision.Image(content=byte_im)

    # Perform label detection
    response = client.label_detection(image=vision_image)
    labels = response.label_annotations

    # Extract the description of the labels
    descriptions = [label.description for label in labels]

    # Join the descriptions into a single string
    image_info = ', '.join(descriptions)

    # Generate a summary using OpenAI's ChatGPT
    messages = [{"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"This image contains the following elements: {image_info}. Please summarize."}]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=100
    )
    summary = response['choices'][0]['message']['content']

    return summary

def gradio_interface():
    image_input = gr.components.Image(type="numpy", label="Image")
    text_output = gr.components.Textbox(label="Summary")

    gr.Interface(fn=analyze_and_summarize, inputs=image_input, outputs=text_output).launch()

if __name__ == "__main__":
    gradio_interface()
