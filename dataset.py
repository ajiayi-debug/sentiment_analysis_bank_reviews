#pip install app_store_scraper
from app_store_scraper import AppStore
import pandas as pd
import numpy as np
import json
#pip install google_play_scraper
from google_play_scraper import app
from google_play_scraper import Sort, reviews_all

gxs = AppStore(country='sg', app_name='gxs-bank', app_id = '1632183616')
gxs.review(how_many=600)

posb = AppStore(country='sg', app_name='posb-digibank', app_id = '1068416633')
posb.review(how_many=1600)

ocbc = AppStore(country='sg', app_name='ocbc-digital-mobile-banking', app_id = '292506828')
ocbc.review(how_many=5000)

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

df2.to_csv('gxs-apple-app-reviews.csv')
# files.download('gxs-apple-app-reviews.csv')



posb_df2.to_csv('posb-apple-app-reviews.csv')
# files.download('posb-apple-app-reviews.csv')



ocbc_df2.to_csv('ocbc-apple-app-reviews.csv')
# files.download('ocbc-apple-app-reviews.csv')

ocbc_df2.rating.unique()


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


df_gxs.to_csv('gxs_playstore2.csv')
# files.download('gxs_playstore2.csv')

# Data Cleaning
gxsapple=pd.read_csv('gxs-apple-app-reviews.csv', index_col=0)
gxsplaystore=pd.read_csv('gxs_playstore2.csv', index_col=0)
posbapple=pd.read_csv('posb-apple-app-reviews.csv', index_col=0)
ocbcapple=pd.read_csv('ocbc-apple-app-reviews.csv', index_col=0)

ocbcapple.rating.unique()

gxsapple['title_review'] = gxsapple['title'] + ' : ' + gxsapple['review']

gxsapple['thumbsUp']= 0

gxsapple['developerResponse'] = gxsapple['developerResponse'].str.replace(r"\{'id': \d+, 'body':", "", regex=True)
gxsapple['developerResponse']=gxsapple['developerResponse'].str.rstrip("}")
gxsapple['developerResponse'] = gxsapple['developerResponse'].str.replace('"', '', regex=False)
gxsapple['developerResponse'] = gxsapple['developerResponse'].str.replace("'", '', regex=False)

gxsapple_dropped = gxsapple.drop(columns=['title', 'review', 'userName', 'isEdited', 'date'])

posbapple['title_review'] = posbapple['title'] + ' : ' + posbapple['review']
posbapple['thumbsUp']= 0
posbapple['developerResponse']=''
posbapple_dropped = posbapple.drop(columns=['title', 'review', 'userName', 'isEdited', 'date'])

ocbcapple['title_review'] = ocbcapple['title'] + ' : ' + ocbcapple['review']
ocbcapple['thumbsUp']= 0
ocbcapple['developerResponse']=''
ocbcapple_dropped = ocbcapple.drop(columns=['title', 'review', 'userName', 'isEdited', 'date'])

gxsplaystore_dropped=gxsplaystore.drop(columns=['reviewId','userName','userImage','reviewCreatedVersion','at','repliedAt','appVersion'])
neworder=['replyContent', 'score', 'content', 'thumbsUpCount']
gxsplaystore_dropped=gxsplaystore_dropped[neworder]

gxsplaystore_dropped.head()

gxsapple_dropped_renamed = gxsapple_dropped.rename(columns={
    'title_review': 'content',
    'thumbsUp': 'thumbsUpCount',
    'developerResponse': 'replyContent',
    'rating': 'score'
})

posbapple_dropped_renamed= posbapple_dropped.rename(columns={
    'title_review': 'content',
    'thumbsUp': 'thumbsUpCount',
    'developerResponse': 'replyContent',
    'rating': 'score'
})

ocbcapple_dropped_renamed= ocbcapple_dropped.rename(columns={
    'title_review': 'content',
    'thumbsUp': 'thumbsUpCount',
    'developerResponse': 'replyContent',
    'rating': 'score'
})

combined_reviews = pd.concat([gxsplaystore_dropped, gxsapple_dropped_renamed, posbapple_dropped_renamed, ocbcapple_dropped_renamed], axis=0, ignore_index=True)

combined_reviews.head()

ocbcapple_dropped_renamed.score.unique() # data cleaning issue

combined_reviews.to_csv("combined_reviews.csv")
# files.download('combined_reviews.csv')

#For finetuning:


datasettrain = pd.concat([posbapple_dropped_renamed, ocbcapple_dropped_renamed], axis=0, ignore_index=True)

datasettest=pd.concat([gxsplaystore_dropped, gxsapple_dropped_renamed], axis=0, ignore_index=True)

datasettrain.to_csv('dataset_train.csv')
datasettest.to_csv('dataset_test.csv')

