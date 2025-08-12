import sys
import os
import numpy as np
import pandas as pd
import praw
from praw import Reddit
from utils.constants import POST_FIELDS

def connect_reddit(client_id, client_secret, user_agent):
    try:
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
        print("✅ Connected to Reddit API")
        return reddit
    except Exception as e:
        print(f"❌ Reddit connection failed: {e}")
        sys.exit(1)

def extract_posts(reddit_instance: Reddit, subreddit: str, time_filter: str, limit=None):
    try:
        subreddit = reddit_instance.subreddit(subreddit)
        posts = subreddit.top(time_filter=time_filter, limit=limit)

        post_lists = []
        for post in posts:
            post_dict = vars(post)
            filtered_post = {key: post_dict.get(key, None) for key in POST_FIELDS}
            post_lists.append(filtered_post)

        print(f"📦 Extracted {len(post_lists)} posts from r/{subreddit}")
        return post_lists
    except Exception as e:
        print(f"❌ Failed to extract posts: {e}")
        return []

def transform_data(post_df: pd.DataFrame):
    try:
        post_df['created_utc'] = pd.to_datetime(post_df['created_utc'], unit='s', errors='coerce')
        post_df['over_18'] = post_df['over_18'].fillna(False).astype(bool)
        post_df['author'] = post_df['author'].astype(str)
        edited_mode = post_df['edited'].mode() 
        post_df['edited'] = np.where(post_df['edited'].isin([True,False]),
                                     post_df['edited'], edited_mode ).astype(bool)
        post_df['num_comments'] = post_df['num_comments'].astype(int)
        post_df['score'] = post_df['score'].astype(int)
        post_df['title'] = post_df['title'].astype(str)
        return post_df
    except Exception as e:
        print(f"❌ Error during transformation: {e}")
        return post_df

def load_data_to_csv(data: pd.DataFrame, path: str):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        data.to_csv(path, index=False)
        print(f"✅ Data saved to: {path}")
    except Exception as e:
        print(f"❌ Failed to write CSV: {e}")
