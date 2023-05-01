# OpenAI Tools

This repository contains a collection of useful scripts related to OpenAI's GPT-4.

## Reddit to Summary Script (reddit2sum.py)

Located in the `reddit` folder, this script uses OpenAI's GPT-4 to summarize Reddit threads. It fetches the top 50 comments from the specified Reddit thread, cleans up the text, and summarizes each chunk of text. The summarized text is then written into a file.

### Prerequisites

- Python 3.8 or above
- PRAW: Python Reddit API Wrapper
- OpenAI Python Client
- python-dotenv

### Setup

1. Clone the repository.
2. Install the required Python libraries using pip:
    ```
    pip install praw openai python-dotenv
    ```
3. Create a `.env` file in your project root and add your Reddit and OpenAI credentials:
    ```
    CLIENT_ID=your_reddit_client_id
    CLIENT_SECRET=your_reddit_client_secret
    USER_AGENT=your_reddit_user_agent
    OPENAI_KEY=your_openai_key
    OPENAI_ORGANIZATION=your_openai_organization
    ```
4. Run the script from within the `reddit` folder:
    ```
    python reddit/reddit2sum_gr.py
    ```

### Usage

When running the script, you will be prompted to enter a Reddit thread ID. The script will then fetch the comments from the thread, summarize them, and write the summaries into a file.
