# GuruBot

GuruBot is a Python-based bot designed to summarize chapters from a book and post those summaries on Twitter in a thread format. The bot utilizes OpenAI's GPT-3.5 for generating summaries and Tweepy for interacting with the Twitter API.

## Features

- Extracts text from a specified range of pages in a PDF file.
- Generates engaging summaries of the extracted text using OpenAI's API.
- Splits the generated summary into multiple tweets.
- Posts the tweets as a thread on Twitter.

## Requirements

- Python 3.7 or higher
- PyMuPDF (fitz)
- OpenAI Python client
- Tweepy

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/GuruBot.git
    cd GuruBot
    ```

2. Install the required packages:
    ```bash
    pip install pymupdf openai tweepy
    ```

## Configuration

1. Set up your OpenAI API key and Twitter API credentials in the script:
    ```python
    # Set your OpenAI API key here
    client = OpenAI(
        api_key='Your_OpenAI_API_Key'
    )

    # Twitter API credentials
    bearer_token = 'Your_Twitter_Bearer_Token'
    consumer_key = 'Your_Twitter_Consumer_Key'
    consumer_secret = 'Your_Twitter_Consumer_Secret'
    access_token = 'Your_Twitter_Access_Token'
    access_token_secret = 'Your_Twitter_Access_Token_Secret'
    ```

2. Define the path to your PDF file and manually identify the chapter page ranges:
    ```python
    pdf_path = r"Path_To_Your_PDF_File.pdf"

    # Manually identified chapter page ranges (start_page, end_page)
    chapter_ranges = [
        (7, 20),   # Chapter 1: Pages 7 to 20
        (21, 34),  # Chapter 2: Pages 21 to 34
        # Add more chapters as needed
    ]
    ```

## Usage

Run the main script to start the summarization and posting process:
```bash
python GuruBot.py
