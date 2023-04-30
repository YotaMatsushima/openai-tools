# YouTube Video Summary Script

This script generates a summary of a YouTube video using OpenAI's GPT-4 model. The script fetches Japanese subtitles from the specified YouTube video, divides the subtitle text into smaller chunks, and generates a summary for each chunk. The final summary is saved in a Markdown file.

## Requirements

* Python 3.6 or higher
* `openai`, `dotenv`, `youtube_transcript_api` Python packages

## Setup

1. Clone this repository and navigate into its directory.
2. Install the required Python packages using pip:

    ```
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the root directory and add your OpenAI API key and organization:

    ```
    OPENAI_KEY=your_openai_key
    OPENAI_ORGANIZATION=your_openai_organization
    ```

## Usage

1. Run the script:

    ```
    python youtube_summary.py
    ```

2. When prompted, enter the URL of the YouTube video you want to summarize. The video must have Japanese subtitles.

The script will create a new Markdown file in the `outputs` directory with the summary of the video. Each summary is separated by two newline characters (`\n\n`).

## Note

This script only supports videos with Japanese subtitles. If you want to summarize videos with subtitles in other languages, you need to modify the `find_transcript(['ja'])` line in the script to use the appropriate language code. Furthermore, the script will throw an error if the video doesn't have subtitles.
