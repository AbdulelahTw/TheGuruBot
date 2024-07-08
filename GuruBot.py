import fitz  # type: ignore # PyMuPDF
import threading
from openai import OpenAI
import re
import time
import tweepy

# Set your OpenAI API key here
client = OpenAI(
    api_key='Your_Key'
)

# Twitter API credentials
bearer_token = 'your_bearer_token'
consumer_key = 'Your_Key'
consumer_secret = 'Your_Key'
access_token = 'Your_Key'
access_token_secret = 'Your_Key'

# Authenticate to Twitter
twitter_client = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

def chat_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-turbo 3.5",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def remove_hashtags(text):
    return re.sub(r'#\w+', '', text).strip()

def split_into_tweets(text, max_length=280):
    tweets = []
    tweet_number = 1
    for tweet in text.split('\n'):
        tweet = tweet.strip()
        if tweet:
            if len(tweet) > max_length - len(f"{tweet_number}/ "):  # account for the "1/ " prefix
                tweet = tweet[:max_length - len(f"{tweet_number}/ ") - 1] + '…'
            tweets.append(f"{tweet_number}/ {tweet}")
            tweet_number += 1
    return tweets

def summarize_chapter(chapter_text, chapter_number):
    try:
        print(f"Summarizing Chapter {chapter_number}...")  # Debug print
        prompt = (
            f"Summarize the following chapter in an engaging and appealing way suitable for a Twitter thread. "
            f"Write the important stuff as if you are a guru or Naval Ravikant. Don't write boring info. "
            f"Each tweet should be around 20 words. Ensure the summary generates a minimum of ten tweets. "
            f"Focus on key insights and appealing points. Do not include any hashtags or promotional content. "
            f"Create a coherent thread that flows well. Remember, tweets have a 280 character limit:\n\n{chapter_text}"
        )
        summary = chat_gpt(prompt)
        tweets = split_into_tweets(summary)
        key_insight = tweets[0] if tweets else ""
        print(f"Chapter {chapter_number} Summary: {tweets}")
        post_tweets(chapter_number, key_insight, tweets)
    except Exception as e:
        print(f"Error summarizing Chapter {chapter_number}: {e}")

def post_tweets(chapter_number, key_insight, tweets):
    first_tweet = f"Chapter {chapter_number} - Key insights from 'The Psychology of Money'\n\n\"{key_insight}\""
    try:
        response = twitter_client.create_tweet(text=first_tweet)
        tweet_id = response.data['id']
        time.sleep(10)
        for tweet in tweets[1:]:  # start from the second tweet as the first one is already included
            print(f"Posting tweet: {tweet}")
            response = twitter_client.create_tweet(text=tweet, in_reply_to_tweet_id=tweet_id)
            tweet_id = response.data['id']
            time.sleep(10)  # Wait for 10 seconds between tweets to avoid rate limits
    except tweepy.TweepyException as e:
        print(f"Error posting tweet: {e}")

def extract_text_from_pdf(pdf_path, start_page, end_page):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(start_page, end_page + 1):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

def main():
    # Define the path to the PDF file
    pdf_path = r"C:\Users\abdul\Desktop\books\The-Psychology-of-Money.pdf"  # Replace with your PDF file path

    # Manually identified chapter page ranges (start_page, end_page)
    chapter_ranges = [
        (7, 20),   # Chapter 1: Pages 7 to 20
                   # Chapter 2: Pages 21 to 34
        # Add more chapters as needed
    ]

    # Create and start a thread for each chapter
    threads = []
    for i, (start_page, end_page) in enumerate(chapter_ranges):
        chapter_text = extract_text_from_pdf(pdf_path, start_page, end_page)
        print(f"Extracted text for Chapter {i + 1} from pages {start_page} to {end_page}")  # Debug print
        thread = threading.Thread(target=summarize_chapter, args=(chapter_text, i + 1))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
