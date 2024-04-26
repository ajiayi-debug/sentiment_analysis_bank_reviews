from app_store_scraper import AppStore
import pandas as pd
import numpy as np
import json
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



df = pd.DataFrame(np.array(gxs.reviews),columns=['review'])
df2 = df.join(pd.DataFrame(df.pop('review').tolist()))

posb_df = pd.DataFrame(np.array(posb.reviews),columns=['review'])
posb_df2 = posb_df.join(pd.DataFrame(posb_df.pop('review').tolist()))

ocbc_df = pd.DataFrame(np.array(ocbc.reviews),columns=['review'])
ocbc_df2 = ocbc_df.join(pd.DataFrame(ocbc_df.pop('review').tolist()))



#google playstore reviews

sg_reviews = reviews_all(
    'sg.com.gxs.app',
    sleep_milliseconds=0, # defaults to 0
    lang='en', # defaults to 'en'
    country='sg', # defaults to 'us'
    sort=Sort.NEWEST, # defaults to Sort.MOST_RELEVANT
)



df_gxs = pd.DataFrame(np.array(sg_reviews),columns=['review'])
df_gxs = pd.DataFrame(df_gxs.pop('review').tolist()) # all rows


# Data Cleaning

gxsapple=df2
gxsplaystore=df_gxs
posbapple=posb_df2
ocbcapple=ocbc_df2

ocbcapple.rating.unique()

gxsapple['title_review'] = gxsapple['title'] + ' : ' + gxsapple['review']

gxsapple['thumbsUp']= 0

gxsapple['developerResponse'] = gxsapple['developerResponse'].apply(lambda x: x.get('body') if isinstance(x, dict) else x)


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



ocbcapple_dropped_renamed.score.unique() # data cleaning issue



#For finetuning:


datasettrain = pd.concat([posbapple_dropped_renamed, ocbcapple_dropped_renamed], axis=0, ignore_index=True)

datasettest=pd.concat([gxsplaystore_dropped, gxsapple_dropped_renamed], axis=0, ignore_index=True)


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
gxsapple.to_sql(name='gxs_apple_app_reviews', con=engine, if_exists='replace', index=False)
posbapple.to_sql(name='posb_apple_app_reviews', con=engine, if_exists='replace', index=False)
ocbcapple.to_sql(name='ocbc_apple_app_reviews', con=engine, if_exists='replace', index=False)
gxsplaystore.to_sql(name='gxs_playstore_app_reviews', con=engine, if_exists='replace', index=False)
datasettest.to_sql(name='datasettest',con=engine, if_exists='replace', index=False)
datasettrain.to_sql(name='datasettrain', con=engine, if_exists='replace', index=False)

engine.dispose()