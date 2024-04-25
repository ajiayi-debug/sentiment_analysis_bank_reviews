# Sentiment Analysis of Customer Feedback

## Background
In today’s digital era, diverse channels such as social media platforms, emails, and customer surveys are being used to provide customer feedback. This has made it a challenge for our orgnanisation to efficiently and accurately analyse the feedback, which is crucial in enabling data-driven decision-making for the company.

This project aims to provide our organisation with an easy and methodical way of analysing customer feedback, and in so doing, enhance customer understanding, improve service quality, and enable data-driven decision-making. To overcome the shortfalls of manual sorting which is time-consuming and error-prone, this project leverages NLP techniques to gauge customer sentiment, identify trends, and highlight areas for improvements.

## Data Scraping
Data scraping for this project was carried out in March 2024. Reviews from various banking apps on the Apple Store and Google Play Store were scraped, and relevant information such as ratings, comments, replies, and thumbs up counts were retained. Other information that contained personal information or were not useful were discarded. The code used for data scraping can be found in [dataset.py](backend/dataset.py). The final dataset was subsequently uploaded to an SQL database for easier access and retrieval.

## Model Description
The code for model training and testing can be found [model_training_and_test.ipynb](backend/model_training_and_test.ipynb).

### Sentiment Analysis
We performed sentiment analysis using a fine-tuned HuggingFace model. For the labels, we used the star ratings of the reviews collected, classifying reviews with more than 3 stars as 'positive' and the rest (≤3 stars) as 'negative'. The fine-tuned model can be found [here](https://huggingface.co/ajiayi/finetuning-sentiment-model-bank_reviews-otherbank)

### Intent Extraction
To extract intent from reviews, we tried a few different methods: text summarisation, topic modelling, and keyword extraction using KeyBERT and rake-nltk. We found that text summarisation did not work well as the reviews were too short, while topic modelling was not feasible as we did not have a predefined topic list that was comprehensive enough. In the end, the keyBERT model was used for intent extraction.

### Summarising Sentiment and Intent
We used a net sentiment figure as a summary of overall sentiment. The net sentiment was used as an alternative to the Net Promoter Score (NPS) as we did not have data specific to the NPS. This metric was referenced from the following [website](https://chattermill.com/blog/nps-calculator#:~:text=Calculating%20your%20net%20promoter%20score,number%20between%20%2D100%20and%20100.).
To summarise overall intent, two dictionaries containing intent keywords associated with positive and negative sentiment reviews respectively were created. These dictionaries were then sorted in descending frequency of keywords.

## GPT
As an extension to our project, we wanted to create a language model that was able to generate replies to reviews. For this, the causal language model from HuggingFace was used, with the baseline model 'openai-community/gpt2'. The code for the finetuning of the GPT can be found [gpt_finetune_causallm.ipynb](backend/gpt_finetune_causallm.ipynb).

## Running the database and application
Use `docker-compose up` to pull mysql image and Dockerfile image creation and create containers for them. Take note that port may need to be changed depending on whether your machine is already using the port. Refer to (docker-compose.yml) on how to change port. Make sure to change the port accordingly in the config file in both backend [config.json(backend)](backend/config.json) as well as in MySQL workbench if you would like to open the database in MySQL workbench. 

To download the data (if you need to get a 'restart' in the database due to accidental deletion etc), run `docker exec -i database_docker sh -c 'exec mysql -u root --password=MYSQL12345' < all_databases.sql`. To get a pure restart (initial condition), make sure you delete any tables that was not there at the start (e.g new_data)

To update the database, run `docker exec database_docker sh -c 'exec mysqldump -u root --password=MYSQL12345 --all-databases' > all_databases.sql`

To open the html frontend webpage, double click the .html file or if in VS code, use the live server extension by Ritwick Dey.

## Using the application
To add new data, format your data according to the template downloadable from upload page. Afterwards, upload your data and wait patiently. You can open another tab with address localhost:3000/new_data and press the refresh button after you upload your data. When the tab reloads successfully and you get an output of 'File uploaded successfully', the data has finished processing and the data has been updated into the database. The new data will add on to the existing data that frontend uses. You can filter for the new data by heading to customer reviews and searching for null in Generated reply content as GPT-2 was not run on the new data due to it being in it's beta phase. 

## Repository Structure
### Backend

| File Name                   | Description                                                                                                    |
|-----------------------------|----------------------------------------------------------------------------------------------------------------|
| dataset.py                  | Code for web-scraping, cleaning, and storing data into the database                                              |
| model_training_and_test.ipynb| Code for training, fine-tuning, and testing of models. Data cleaning for fine-tuning and benchmarking of reviews is done here |
| finetune_bert.ipynb         | Code for fine-tuning DistilBERT and data cleaning for fine-tuning                                                 |
| gpt_finetune_causallm.ipynb | Code for fine-tuning GPT-2 with GXS reviews and replies                                                           |
| scrape_all.ipynb            | Code for running chosen models on GXS reviews and getting output summary, sent to frontend for data visualization|
| app.py                      | Code for Flask that connects backend to frontend through data sharing                                             |
| requirements.txt            | Code to install dependencies used in the app, automatically run during Docker compose                               |
| config.json                 | Configuration for the MySQL database on a local machine                                                           |
| gpt_model_causallm (folder) | Configuration for fine-tuned GPT-2 model and its safetensors                                                        |
| newdata.py                  | Code for running DistilBERT (fine-tuned) and KeyBERT on newly uploaded data by users                              |

### Frontend

| File Name           | Description                                                                                                                            |
|---------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| customer_review.js  | Code for displaying customer reviews on the corresponding webpage, with data processing functions                                       |
| customer_reviews.html| Code for webpage aesthetics (customer reviews section)                                                                                   |
| dashboard.js        | Code for the dashboard showing data visualizations, sentiment summaries, and count of reviews                                             |
| index.html          | Code for webpage aesthetics (dashboard)                                                                                                   |
| scripts.js          | Code for the left sidebar functionality                                                                                                  |
| settings.json       | Code for setting the port for the frontend live server                                                                                   |
| template.csv        | Template CSV file for users to download and structure their data                                                                          |
| upload_csv.html     | Code for webpage aesthetics (file upload section)                                                                                         |
| upload_csv.js       | Code for sending uploaded CSV to the backend through Flask, and allowing users to download `template.csv`                                 |
| wordcloud.html      | Code for the aesthetics of the word cloud                                                                                                |
| wordcloud.js        | Code that uses summary data keywords to generate the word cloud                                                                          |

### Software Requirements

| Package                  | Version |
|--------------------------|---------|
| accelerate               | 0.29.3  |
| app_store_scraper        | 0.3.5   |
| bertopic                 | 0.16.0  |
| datasets                 | 2.18.0  |
| flask                    | 2.2.2   |
| flask-cors               | 4.0.0   |
| google_play_scraper      | 1.2.6   |
| huggingface_hub          | 0.22.2  |
| keybert                  | 0.8.4   |
| pandas                   | 1.5.3   |
| mysql-connector-python   | 8.3.0   |
| numpy                    | 1.23.5  |
| rake-nltk                | 1.0.6   |
| scikit-learn             | 1.2.1   |
| seaborn                  | 0.12.2  |
| sqlalchemy               | 1.4.39  |
| transformers             | 4.39.3  |
| tqdm                     | 4.66.2  |
| werkzeug                 | 2.2.2   |

