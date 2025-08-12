from utils.constants import CLIENT_ID, SECRET, OUTPUT_PATH
from etls.reddit_etl import connect_reddit, extract_posts, transform_data, load_data_to_csv
import pandas as pd
import os

def redditpipeline(file_name: str, subreddit: str, time_filter='day', limit=None):
    # Connect to Reddit instance
    instance = connect_reddit(CLIENT_ID, SECRET, 'RheaSanthmayorScript')
    
    # Extract posts
    posts = extract_posts(instance, subreddit, time_filter, limit)
    post_df = pd.DataFrame(posts)
    
    # Transform data
    post_df = transform_data(post_df)
    
    # Ensure the output directory exists
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    
    # Construct full file path and save
    file_path = os.path.join(OUTPUT_PATH, f'{file_name}.csv')
    load_data_to_csv(post_df, file_path)

    return file_path
