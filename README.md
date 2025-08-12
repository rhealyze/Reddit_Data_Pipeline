"# Reddit_Data_Pipeline" 
"# Reddit_Data_Pipeline" 
Reddit ETL Pipeline
A fully automated data pipeline that extracts Reddit posts from specified subreddits, transforms and cleans the data, then uploads the results to AWS S3. The pipeline is orchestrated with Apache Airflow for scheduled execution.

Features
Extracts top posts from Reddit using the Reddit API (PRAW).

Cleans and transforms raw post data into structured CSV files.

Uploads processed files to an AWS S3 bucket for storage or analysis.

Configurable via external .conf files for credentials and file paths.

Scheduled and managed with Airflow DAG for daily automated runs.




Pipeline Flow Diagram
![Reddit ETL Pipeline Flow](RedditDataEngineering.png)
