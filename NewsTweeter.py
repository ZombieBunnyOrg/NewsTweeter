import openai
import requests
from datetime import date
from datetime import timedelta
import tweepy
import os
import sys
import random
import contextlib
import json
from urllib.parse import urlencode         
from urllib.request import urlopen


# Azure OpenAI Info
ENDPOINT = "XXX"
AZURE_API_KEY = "XXX"
DEPLOYMENT = "GPT35"


def make_tiny(url):
    request_url = ('http://tinyurl.com/api-create.php?' + urlencode({'url':url}))  
    with contextlib.closing(urlopen(request_url)) as response:                     
        return response.read().decode('utf-8 ')

try:
    topic_index = int(sys.argv[1])
    #topic_index = 4
    if topic_index == 1:
        url = f"https://newsdata.io/api/1/news?apikey=XXXXXXXXXXXX&country=us&language=en&category=tourism"
    elif topic_index == 2:
        url = "https://newsdata.io/api/1/news?apikey=XXXXXXXXXXXX&country=us&language=en&category=technology"
    elif topic_index == 3:
        url = "https://newsdata.io/api/1/news?apikey=XXXXXXXXXXXX&country=us&language=en&category=entertainment"
    elif topic_index == 4:
        url = "https://newsdata.io/api/1/news?apikey=XXXXXXXXXXXX&country=us&language=en&category=business"
    elif topic_index == 5:
        url = "https://newsdata.io/api/1/news?apikey=XXXXXXXXXXXX&country=us&language=en&category=top"


except:
    print("Argument 1 = tourism, 2 = technology or 3 = entertainment or 4 = business or 5 = top is neeeded")
    exit()

response = requests.get(url)
top_news = response.json()

artical_num = random.randint(0, len(top_news["results"]) - 1)

# Select the first news article
article = top_news['results'][artical_num]

tinyurl = make_tiny(article['link'])

#Azure Version of Open API
openai.api_type = "azure"
openai.api_base = ENDPOINT
openai.api_version = "2023-03-15-preview"
openai.api_key = AZURE_API_KEY

prompt = (f"Write an informative and playful tweet about the following news article located at the URL {article['link']} which has the title \"{article['title']}\" and a description of \"{article['description']}\" and content of \"{article['content']}\".  Include a reference to the article using the tinyurl {tinyurl} as well as relevant hashtags related to the article. Once complete include \"https://zombiebunny.org\" and \"#ZombieBunnyOrg\" at the end. The total tweet length must be less than 250 characters.")


response = openai.ChatCompletion.create(
    engine=DEPLOYMENT,
    messages=[
        {"role": "system", "content": "You are a helpful assistant that creates twitter posts."},
        {"role": "user", "content": prompt},
    ]
)

message = response['choices'][0]['message']['content']

# Set up the Twitter API client
API_KEY = "XXX"
API_KEY_SECRET = "XXX"
Bearer_Token = "XXX"
CLIENT_ID = "XXX"
CLIENT_SECRET = "XXX"
ACCESS_TOKEN = "XXX"
ACCESS_TOKEN_SECRET = "XXX"

# Set up the OAuth2 authentication
auth = tweepy.OAuth1UserHandler(API_KEY, API_KEY_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Connect to the API
api = tweepy.API(auth)

len(message)

# Create a tweet
api.update_status(message)