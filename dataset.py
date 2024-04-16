#pip install app_store_scraper
from app_store_scraper import AppStore
import pandas as pd
import numpy as np
import json
#pip install google_play_scraper
from google_play_scraper import app
from google_play_scraper import Sort, reviews_all
import mysql.connector as mysql
from sqlalchemy import create_engine


gxs = AppStore(country='sg', app_name='gxs-bank', app_id = '1632183616')
gxs.review(how_many=600)

posb = AppStore(country='sg', app_name='posb-digibank', app_id = '1068416633')
posb.review(how_many=1600)

ocbc = AppStore(country='sg', app_name='ocbc-digital-mobile-banking', app_id = '292506828')
ocbc.review(how_many=5000)


# def fetch_reviews(app_store_instance, how_many, retries=5, delay=10):
#     try:
#         # Attempt to fetch the reviews
#         app_store_instance.review(how_many=how_many)
#     except Exception as e:
#         if retries > 0:
#             print(f"Error fetching reviews: {e}. Retrying in {delay} seconds...")
#             time.sleep(delay)
#             fetch_reviews(app_store_instance, how_many, retries-1, delay*random.uniform(1.5, 2))
#         else:
#             print("Max retries reached. Failed to fetch all reviews.")


# gxs = AppStore(country='sg', app_name='gxs-bank', app_id='1632183616')
# posb = AppStore(country='sg', app_name='posb-digibank', app_id='1068416633')
# ocbc = AppStore(country='sg', app_name='ocbc-digital-mobile-banking', app_id='292506828')

# Fetch reviews with retry logic
# gxs=fetch_reviews(gxss, 600)
# posb=fetch_reviews(posbb, 1600)
# ocbc=fetch_reviews(ocbcc, 5000)

# ocbc = AppStore(country='sg', app_name='ocbc-digital-mobile-banking', app_id = '292506828')
# ocbc.review(how_many=2000)

df = pd.DataFrame(np.array(gxs.reviews),columns=['review'])
df2 = df.join(pd.DataFrame(df.pop('review').tolist()))
#df2.head()

posb_df = pd.DataFrame(np.array(posb.reviews),columns=['review'])
posb_df2 = posb_df.join(pd.DataFrame(posb_df.pop('review').tolist()))
#posb_df2.head()

ocbc_df = pd.DataFrame(np.array(ocbc.reviews),columns=['review'])
ocbc_df2 = ocbc_df.join(pd.DataFrame(ocbc_df.pop('review').tolist()))
#ocbc_df2.head()

# df2.to_csv('gxs-apple-app-reviews.csv')
# files.download('gxs-apple-app-reviews.csv')



#posb_df2.to_csv('posb-apple-app-reviews.csv')
# files.download('posb-apple-app-reviews.csv')



#ocbc_df2.to_csv('ocbc-apple-app-reviews.csv')
# files.download('ocbc-apple-app-reviews.csv')

#ocbc_df2.rating.unique()


#google playstore reviews

sg_reviews = reviews_all(
    'sg.com.gxs.app',
    sleep_milliseconds=0, # defaults to 0
    lang='en', # defaults to 'en'
    country='sg', # defaults to 'us'
    sort=Sort.NEWEST, # defaults to Sort.MOST_RELEVANT
)



df_gxs = pd.DataFrame(np.array(sg_reviews),columns=['review'])
# df_gxs = df.join(pd.DataFrame(df_gxs.pop('review').tolist())) # missing ~60+ rows, not sure why
df_gxs = pd.DataFrame(df_gxs.pop('review').tolist()) # all rows


#df_gxs.to_csv('gxs_playstore2.csv')
# files.download('gxs_playstore2.csv')

# Data Cleaning
# gxsapple=pd.read_csv('gxs-apple-app-reviews.csv', index_col=0)
# gxsplaystore=pd.read_csv('gxs_playstore2.csv', index_col=0)
# posbapple=pd.read_csv('posb-apple-app-reviews.csv', index_col=0)
# ocbcapple=pd.read_csv('ocbc-apple-app-reviews.csv', index_col=0)

gxsapple=df2
gxsplaystore=df_gxs
posbapple=posb_df2
ocbcapple=ocbc_df2

ocbcapple.rating.unique()

gxsapple['title_review'] = gxsapple['title'] + ' : ' + gxsapple['review']

gxsapple['thumbsUp']= 0

gxsapple['developerResponse'] = gxsapple['developerResponse'].apply(lambda x: x.get('body') if isinstance(x, dict) else x)
# gxsapple['developerResponse'] = gxsapple['developerResponse'].str.replace(r"\{'id': \d+, 'body':", "", regex=True)
# gxsapple['developerResponse']=gxsapple['developerResponse'].str.rstrip("}")
# gxsapple['developerResponse'] = gxsapple['developerResponse'].str.replace('"', '', regex=False)
# gxsapple['developerResponse'] = gxsapple['developerResponse'].str.replace("'", '', regex=False)


gxsapple_dropped = gxsapple.drop(columns=['title', 'review', 'userName', 'isEdited'])

posbapple['title_review'] = posbapple['title'] + ' : ' + posbapple['review']
posbapple['thumbsUp']= 0
posbapple['developerResponse']=''
posbapple_dropped = posbapple.drop(columns=['title', 'review', 'userName', 'isEdited'])

ocbcapple['title_review'] = ocbcapple['title'] + ' : ' + ocbcapple['review']
ocbcapple['thumbsUp']= 0
ocbcapple['developerResponse']=''
ocbcapple_dropped = ocbcapple.drop(columns=['title', 'review', 'userName', 'isEdited'])

gxsplaystore_dropped=gxsplaystore.drop(columns=['reviewId','userName','userImage','reviewCreatedVersion','repliedAt','appVersion'])
neworder=['replyContent', 'score', 'content', 'thumbsUpCount']
gxsplaystore_dropped=gxsplaystore_dropped[neworder]



gxsplaystore_dropped=gxsplaystore_dropped.rename(columns={
    'content': 'content',
    'thumbsUpCount': 'thumbsUpCount',
    'replyContent': 'replyContent',
    'score': 'score',
    'at':'date'
})

gxsapple_dropped_renamed = gxsapple_dropped.rename(columns={
    'title_review': 'content',
    'thumbsUp': 'thumbsUpCount',
    'developerResponse': 'replyContent',
    'rating': 'score',
    'date':'date'
})

posbapple_dropped_renamed= posbapple_dropped.rename(columns={
    'title_review': 'content',
    'thumbsUp': 'thumbsUpCount',
    'developerResponse': 'replyContent',
    'rating': 'score',
    'date':'date'

})

ocbcapple_dropped_renamed= ocbcapple_dropped.rename(columns={
    'title_review': 'content',
    'thumbsUp': 'thumbsUpCount',
    'developerResponse': 'replyContent',
    'rating': 'score',
    'date':'date'
})

combined_reviews = pd.concat([gxsplaystore_dropped, gxsapple_dropped_renamed, posbapple_dropped_renamed, ocbcapple_dropped_renamed], axis=0, ignore_index=True)
if combined_reviews['replyContent'].apply(lambda x: isinstance(x, dict)).any():
    combined_reviews['replyContent'] = combined_reviews['replyContent'].apply(lambda x: json.dumps(x) if isinstance(x, dict) else x)

print(combined_reviews.head())

ocbcapple_dropped_renamed.score.unique() # data cleaning issue

#combined_reviews.to_csv("combined_reviews.csv")
# files.download('combined_reviews.csv')

#For finetuning:


datasettrain = pd.concat([posbapple_dropped_renamed, ocbcapple_dropped_renamed], axis=0, ignore_index=True)

datasettest=pd.concat([gxsplaystore_dropped, gxsapple_dropped_renamed], axis=0, ignore_index=True)

#datasettrain.to_csv('dataset_train.csv')
#datasettest.to_csv('dataset_test.csv')


# #Sending data to mysql database

# user = 'root'
# password = 'SQL12345'
# host = 'ec2-13-212-240-70.ap-southeast-1.compute.amazonaws.com'
# database = 'database'

# # Create a connection string
# conn_string = f'mysql+mysqlconnector://{user}:{password}@{host}/{database}'

# # Create an engine
# engine = create_engine(conn_string)

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

combined_reviews.to_sql(name='combined_reviews', con=engine, if_exists='replace', index=False)
gxsapple.to_sql(name='gxs-apple-app-reviews', con=engine, if_exists='replace', index=False)
posbapple.to_sql(name='posb-apple-app-reviews', con=engine, if_exists='replace', index=False)
ocbcapple.to_sql(name='ocbc-apple-app-reviews', con=engine, if_exists='replace', index=False)
gxsplaystore.to_sql(name='gxs-playstore-app-reviews', con=engine, if_exists='replace', index=False)
datasettest.to_sql(name='datasettest',con=engine, if_exists='replace', index=False)
datasettrain.to_sql(name='datasettrain', con=engine, if_exists='replace', index=False)

engine.dispose()