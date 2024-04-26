import json
import pandas as pd
from sqlalchemy import create_engine
from transformers import pipeline
from keybert import KeyBERT
from tqdm import tqdm

# Load database configuration
CONFIG_FILE = 'config.json'

def load_db_config():
    with open(CONFIG_FILE) as config_file:
        config = json.load(config_file)
    return config['database']

def get_sqlalchemy_engine(db_config):
    user = db_config['user']
    password = db_config['password']
    host = db_config['host']
    port = db_config.get('port',3306)  # Default to MySQL port 3306
    database = db_config['database']
    conn_string = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
    return create_engine(conn_string)

# Fetching Data
def fetch_data(engine, query):
    return pd.read_sql(query, con=engine)

# Sentiment Analysis and Keyword Extraction
def analyze_data(dataset):
    sentiment_pipeline = pipeline("sentiment-analysis", model='ajiayi/finetuning-sentiment-model-bank_reviews-otherbank')
    ke_model = KeyBERT()

    sentiments = []
    keywords = []
    replies=[]

    for _, row in tqdm(dataset.iterrows(), total=len(dataset)):
        review = row['content']

        # Perform Sentiment Analysis
        sentiment_result = sentiment_pipeline(review)[0]['label']
        sentiments.append(sentiment_result)

        # Extract Keywords
        keyword_result = ke_model.extract_keywords(review, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=1)
        keywords.append(keyword_result[0][0] if keyword_result else '')
        replies.append('null')

    dataset['sentiment'] = sentiments
    dataset['keywords'] = keywords
    dataset['replies']=replies

    return dataset

# Summarizing Sentiment
def summarize_sentiment(reviews):
    ns_score = 0
    neg_keywords = {}
    pos_keywords = {}

    for _, row in reviews.iterrows():
        sentiment = row['sentiment']
        word = row['keywords']
        
        if sentiment == 'POSITIVE':
            ns_score += 1
            if word in pos_keywords:
                pos_keywords[word] += 1
            else:
                pos_keywords[word] = 1
        else:
            ns_score -= 1
            if word in neg_keywords:
                neg_keywords[word] += 1
            else:
                neg_keywords[word] = 1

    total = len(reviews)
    ns_score = (ns_score / total) * 100

    pos_keywords = {k: v for k, v in sorted(pos_keywords.items(), key=lambda item: item[1], reverse=True)}
    neg_keywords = {k: v for k, v in sorted(neg_keywords.items(), key=lambda item: item[1], reverse=True)}

    return ns_score, pos_keywords, neg_keywords

# Main Execution
def main():
    db_config = load_db_config()
    engine = get_sqlalchemy_engine(db_config)

    try:
        # Step 1: Fetch Data and Process It
        query = "SELECT * FROM new_data"
        dataset = fetch_data(engine, query)
        if 'Unnamed: 0' in dataset.columns:
            dataset = dataset.drop(columns=['Unnamed: 0'])
        dataset = analyze_data(dataset)
        dataset = dataset.rename(columns={'replies':'generatedReply'})

        # Step 2: Store Processed Data Back to Database
        dataset.to_sql(name='sentiment_data', con=engine, if_exists='append', index=False)

        # Step 3: Retrieve Stored Data for Summary function
        stored_dataset = fetch_data(engine, "SELECT * FROM sentiment_data")

        # Step 4: Summarize the Sentiment
        summaries = summarize_sentiment(stored_dataset)

        positive_df = pd.DataFrame(list(summaries[1].items()), columns=['keyword', 'count'])
        negative_df = pd.DataFrame(list(summaries[2].items()), columns=['keyword', 'count'])
        positive_df['netSentiment'] = summaries[0]  # Add netSentiment as a column to positive_df
        negative_df['netSentiment'] = summaries[0]  # Add netSentiment as a column to negative_df

        positive_df['sentiment'] = 'positive'
        negative_df['sentiment'] = 'negative'

        summary_df = pd.concat([positive_df, negative_df], ignore_index=True)

        # Step 5: Store Summary Back to Database
        summary_df.to_sql(name='summary', con=engine, if_exists='replace', index=False)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        engine.dispose()  # Ensure connection closure

# Run the script
if __name__ == "__main__":
    main()
