#sentiment
#pip install transformers
#pip install -U bertopic
from bertopic import BERTopic
#pip install keybert
from keybert import KeyBERT
# pip install rake-nltk
# pip install nltk
from rake_nltk import Rake
import nltk
from transformers import pipeline
import pandas as pd
import seaborn as sns
import mysql.connector
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
import json
import pandas as pd

# # Load database configuration from JSON file
# with open('config.json') as config_file:
#     config = json.load(config_file)['database']

# # Establish a connection using the loaded configuration
# cnx = mysql.connector.connect(**config)

# # Define your query
# query = f"SELECT * FROM combined_reviews"

# # Use pandas to load sql query into a DataFrame
# dataset = pd.read_sql(query, con=cnx)

# # Don't forget to close the connection when done
# cnx.close()


dataset = pd.read_csv("combined_reviews.csv", index_col=0)

dataset.score.unique()

dataset[dataset.score.isna()==True]

#sns.histplot(dataset.score) # uneven spread of ratings (mostly 1 or 5)

score_sentiment = []
for score in dataset.score:
  if score > 3:
    score_sentiment.append(1) # Positive
  # elif score == 3:
  #   score_sentiment.append(0) # Neutral
  else:
    score_sentiment.append(-1) # Negative

dataset['score_sentiment'] = score_sentiment

dataset['score_sentiment'].value_counts()


dataset.to_csv("sentiment.csv")

# Load database configuration from JSON file
with open('config.json') as config_file:
    config = json.load(config_file)['database']

# Construct the connection string using the loaded configuration
user = config['user']
password = config['password']
host = config['host']
dbname = config['database']
port = config['port']
conn_string = f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{dbname}'

# Create an engine
engine = create_engine(conn_string)

dataset.to_sql(name='sentiment', con=engine, if_exists='replace', index=False)


engine.dispose()

##TO CALL THE SENTIMENT AS A CSV, REFER TO MYSQLTOCSVTEST>PY



def sentiment_accuracy(model):
  sentiment_pipeline = pipeline("sentiment-analysis", model=model)
  count = 0

  for row in range(len(dataset.content)):
    pred_sentiment = sentiment_pipeline(dataset.content[row])[0]['label']
    pred_sentiment = define(pred_sentiment)
    if pred_sentiment == dataset.score_sentiment[row]:
      count += 1

  acc = count/len(dataset.content)
  return acc

# baseline model
baseline_model = 'distilbert/distilbert-base-uncased-finetuned-sst-2-english'

def define(pred):
  if pred == 'POSITIVE': return 1
  # elif pred == 'NEGATIVE': return -1
  else: return -1

sentiment_accuracy(baseline_model)

# fin model
fin_model = 'yiyanghkust/finbert-tone'

def define(pred):
  if pred == 'Positive': return 1
  # elif pred == 'Negative': return -1
  else: return -1

sentiment_accuracy(fin_model)

#Finetuning

# Load database configuration from JSON file
with open('config.json') as config_file:
    config = json.load(config_file)['database']

# Establish a connection using the loaded configuration
cnx = mysql.connector.connect(**config)

# Define your query
query = f"SELECT * FROM datasettest"

# Use pandas to load sql query into a DataFrame
datasettest = pd.read_sql(query, con=cnx)


# Don't forget to close the connection when done
cnx.close()

import mysql.connector
import pandas as pd

# Load database configuration from JSON file
with open('config.json') as config_file:
    config = json.load(config_file)['database']

# Establish a connection using the loaded configuration
cnx = mysql.connector.connect(**config)

# Define your query
query = f"SELECT * FROM datasettrain"

# Use pandas to load sql query into a DataFrame
datasettrain = pd.read_sql(query, con=cnx)

# Don't forget to close the connection when done
cnx.close()

# datasettrain = pd.read_csv('dataset_train.csv')

# datasettest=pd.read_csv('dataset_test.csv')

score_sentiment_train = []
for score in datasettrain.score:
  if score > 3:
    score_sentiment_train.append(1) # Positive
  else:
    score_sentiment_train.append(0) # Negative

score_sentiment_test = []
for score in datasettest.score:
  if score > 3:
    score_sentiment_test.append(1) # Positive
  else:
    score_sentiment_test.append(0) # Negative

datasettrain['score_sentiment'] = score_sentiment_train
datasettest['score_sentiment']=score_sentiment_test


"below is finetuning already done. just continue on to use the finetuned model"
# # baseline model train
# baseline_model_train = 'distilbert/distilbert-base-uncased-finetuned-sst-2-english'

# finetune=datasettrain.drop(columns=['replyContent','thumbsUpCount','score'])
# finetune=finetune.rename(columns={
#     'content':'text',
#     'score_sentiment':'label'
# })



# finetune.to_csv('finetune.csv')

# #For fine tuning
# pip install datasets
# import pandas as pd
# from datasets import Dataset, DatasetDict
# from sklearn.model_selection import train_test_split

# # Step 1: Load your CSV file into a Pandas DataFrame
# df = pd.read_csv('finetune.csv')
# # Columns to remove
# columns_to_remove = ['Unnamed: 0.1', 'Unnamed: 0', '__index_level_0__']

# # Only drop columns which are present in the DataFrame
# df = df.drop(columns=[col for col in columns_to_remove if col in df.columns])
# # Step 2: Convert the DataFrame to a Hugging Face `Dataset`
# dataset_huggingface = Dataset.from_pandas(df)

# # Split your DataFrame into training and testing sets 
# train_df, test_df = train_test_split(df, test_size=0.1)  

# # Convert the train and test DataFrames to Datasets
# train_dataset = Dataset.from_pandas(train_df)
# train_dataset = train_dataset.remove_columns('__index_level_0__')
# test_dataset = Dataset.from_pandas(test_df)
# test_dataset = test_dataset.remove_columns('__index_level_0__')

# # Convert to DatasetDict (if needed for convenience)
# dataset_dict = DatasetDict({
#     'train': train_dataset,
#     'test': test_dataset
# })

# # Shuffle and select small subsets for fine-tuning (as examples)
# small_train_dataset = dataset_dict['train'].shuffle(seed=42).select(range(1008))
# small_test_dataset = dataset_dict['test'].shuffle(seed=42).select(range(112))

# # Example output
# print(small_train_dataset[0])
# print(small_test_dataset[0])

# from transformers import AutoTokenizer
# tokenizer = AutoTokenizer.from_pretrained(baseline_model_train)

# def preprocess_function(examples):
#     return tokenizer(examples['text'], truncation=True)

# tokenized_train = small_train_dataset.map(preprocess_function, batched=True)
# tokenized_test = small_test_dataset.map(preprocess_function, batched=True)

# from transformers import DataCollatorWithPadding
# data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

# from transformers import AutoModelForSequenceClassification
# model = AutoModelForSequenceClassification.from_pretrained(baseline_model_train, num_labels=2)

# # Define the evaluation metrics
# import numpy as np
# from datasets import load_metric

# def compute_metrics(eval_pred):
#     load_accuracy = load_metric("accuracy")
#     load_f1 = load_metric("f1")

#     logits, labels = eval_pred
#     predictions = np.argmax(logits, axis=-1)
#     accuracy = load_accuracy.compute(predictions=predictions, references=labels)["accuracy"]
#     f1 = load_f1.compute(predictions=predictions, references=labels)["f1"]
#     return {"accuracy": accuracy, "f1": f1}


# # Get your API token here https://huggingface.co/settings/token
# from huggingface_hub import notebook_login

# notebook_login()

# pip install accelerate -U

# from transformers import TrainingArguments, Trainer

# repo_name = "finetuning-sentiment-model-bank_reviews-otherbank"

# training_args = TrainingArguments(
#     output_dir=repo_name,
#     learning_rate=2e-5,
#     per_device_train_batch_size=16,
#     per_device_eval_batch_size=16,
#     num_train_epochs=2,
#     weight_decay=0.01,
#     save_strategy="epoch",
#     push_to_hub=True,
# )

# trainer = Trainer(
#     model=model,
#     args=training_args,
#     train_dataset=tokenized_train,
#     eval_dataset=tokenized_test,
#     tokenizer=tokenizer,
#     data_collator=data_collator,
#     compute_metrics=compute_metrics,
# )

# trainer.train()

# trainer.evaluate()

# trainer.push_to_hub()


# from transformers import pipeline

# sentiment_model = pipeline(model="ajiayi/finetuning-sentiment-model-bank_reviews-otherbank")

# sentiment_model(["I love this move", "This movie sucks!"])

def sentiment_accuracy_test(model):
  sentiment_pipeline = pipeline("sentiment-analysis", model=model)
  count = 0

  for row in range(len(datasettest.content)):
    pred_sentiment = sentiment_pipeline(datasettest.content[row])[0]['label']
    pred_sentiment = define(pred_sentiment)
    if pred_sentiment == datasettest.score_sentiment[row]:
      count += 1

  acc = count/len(datasettest.content)
  return acc

#finetuned version of baseline model

# baseline model train
baseline_model_finetune = 'ajiayi/finetuning-sentiment-model-bank_reviews-otherbank'

def define(pred):
  if pred == 'POSITIVE': return 1
  elif pred == 'NEGATIVE': return 0


sentiment_accuracy_test(baseline_model_finetune)

"""# Text analysis to obtain intent/insight
Possible ideas:
- Topic modelling
- Text summarisation

Keyword extraction techniques: https://www.analyticsvidhya.com/blog/2022/03/keyword-extraction-methods-from-documents-in-nlp/
"""

dataset.content[1]

# text summarization, doesn't really work since sentences are too short
summarizer = pipeline("summarization", min_length=0, max_length=15)
summarizer(dataset.content[1])

# topic modelling, idk.. doesn't seem to work too well on predefined topic list
topic_model = BERTopic.load("davanstrien/transformers_issues_topics")
topic, prob = topic_model.transform(dataset.content[1])

# keyword extraction, keyBERT
kw_model = KeyBERT()
keywords = kw_model.extract_keywords(dataset.content[1])
print(keywords)

# keyword extraction, rake-nltk
nltk.download('stopwords')
nltk.download('punkt')
r=Rake()
r.extract_keywords_from_text(dataset.content[1])
r.get_ranked_phrases()

"""Topic modelling (for data analysis) https://huggingface.co/heyitskim1912/TopicModelling
If we use gpt to reply to reviews, technically dunnid topic modelling, topic modelling will then be used more for data visualisation. (or can use to make life of gpt easier lol)

# Net Sentiment + Frequency of Words/Intents

Alternative to NPS since we don't have raw data for NPS

https://chattermill.com/blog/nps-calculator#:~:text=Calculating%20your%20net%20promoter%20score,number%20between%20%2D100%20and%20100.
"""
# Load database configuration from JSON file
with open('config.json') as config_file:
    config = json.load(config_file)['database']

# Establish a connection using the loaded configuration
cnx = mysql.connector.connect(**config)

# Define your query
query = f"SELECT * FROM gxs-apple-app-reviews"

# Use pandas to load sql query into a DataFrame
gxs_apple_app_gxs_reviews = pd.read_sql(query, con=cnx)

# Don't forget to close the connection when done
cnx.close()
gxsapple=gxs_apple_app_gxs_reviews

gxsapple['title_review'] = gxsapple['title'] + ' : ' + gxsapple['review']

gxsapple['thumbsUp']= 0

gxsapple['developerResponse'] = gxsapple['developerResponse'].apply(lambda x: x.get('body') if isinstance(x, dict) else x)

gxsapple_dropped = gxsapple.drop(columns=['title', 'review', 'userName', 'isEdited'])

gxsapple_dropped_renamed = gxsapple_dropped.rename(columns={
    'title_review': 'content',
    'thumbsUp': 'thumbsUpCount',
    'developerResponse': 'replyContent',
    'rating': 'score',
    'date':'date'
})


# Load database configuration from JSON file
with open('config.json') as config_file:
    config = json.load(config_file)['database']

# Establish a connection using the loaded configuration
cnx = mysql.connector.connect(**config)

# Define your query
query = f"SELECT * FROM gxs-playstore-app-reviews"

# Use pandas to load sql query into a DataFrame
gxs_playstore_app_gxs_reviews = pd.read_sql(query, con=cnx)

# Don't forget to close the connection when done
cnx.close()

gxsplaystore_dropped=gxs_playstore_app_gxs_reviews.drop(columns=['reviewId','userName','userImage','reviewCreatedVersion','repliedAt','appVersion'])
neworder=['replyContent', 'score', 'content', 'thumbsUpCount']
gxsplaystore_dropped=gxsplaystore_dropped[neworder]



gxsplaystore_dropped=gxsplaystore_dropped.rename(columns={
    'content': 'content',
    'thumbsUpCount': 'thumbsUpCount',
    'replyContent': 'replyContent',
    'score': 'score',
    'at':'date'
})


gxs_reviews = pd.concat([gxsplaystore_dropped, gxsapple_dropped_renamed], axis=0, ignore_index=True)

def summarise_sentiment(reviews): #havent test this fn

  '''
  Input:
  - reviews: dataset containing at least the following 2 columns ['content', 'thumbsUpCount']
  Output:
  - net sentiment score: numeric, between -100 and +100
  - neg_keywords: dictionary containing negative keywords, sorted descending
  - pos_keywords: dictionary containing positive keywords, sorted descending
  '''

  model = 'ajiayi/finetuning-sentiment-model-bank_reviews-otherbank' # maybe need to streamline this && change to trained model
  sentiment_pipeline = pipeline("sentiment-analysis", model=model)
  ns_score = 0

  kw_model = KeyBERT() # check if this is the best model to use
  neg_keywords = {}
  pos_keywords = {}

  for row in range(len(reviews)):
    pred_sentiment = sentiment_pipeline(reviews.content[row])[0]['label']
    keywords = kw_model.extract_keywords(reviews.content[row])
    if pred_sentiment == 'POSITIVE':
      pred_sentiment = 1
      for word in keywords:
        if word in pos_keywords:
          pos_keywords[word] += 1
        else:
          pos_keywords[word] = 1
    else:
      pred_sentiment = -1
      for word in keywords:
        if word in neg_keywords:
          neg_keywords[word] += 1
        else:
          neg_keywords[word] = 1
    ns_score += pred_sentiment * (reviews.thumbsUpCount[row]+1) # need to vectorise for faster runtime

  total = sum(reviews.thumbsUpCount) + len(reviews)
  ns_score = ns_score/total*100

  pos_keywords = dict(sorted(pos_keywords.items(), key=lambda x: x[1], reverse = True))
  neg_keywords = dict(sorted(neg_keywords.items(), key=lambda x: x[1], reverse = True))

  return ns_score, pos_keywords, neg_keywords

summarise_sentiment(gxs_reviews)


