
import tweepy
import openai
import pandas as pd
import seaborn as sns

# Your openAi API credentials
openai.api_key = "put your openai key herr"

# Your Twitter API credentials 
consumer_key = "put your consumer key here"
consumer_secret = "put your consumer secret here"
access_token = "put your access token here"
access_token_secret = "put your access token secret here"


# Authenticate to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create API object
api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication Succesful")
    auth_status = True
except Exception as e:
    print("Error during authentication: %s" % e)
    auth_status = False

# Use the API to search for tweets containing "$BTC" hashtag
KEYWORDS = "bitcoin" 
tweetBag = []

if auth_status:
    try:
       
        tweets = api.search_tweets(KEYWORDS, result_type="recent", count=25, tweet_mode="extended")
        #tweets = api.search_tweets(KEYWORDS, result_type="popular", tweet_mode="extended")
        #tweets = api.search_tweets(KEYWORDS, result_type="mixed", tweet_mode="extended")

        for tweet in tweets:
            text_leng = len(tweet.full_text.split())
            if (not tweet.retweeted and tweet.user.followers_count >= 10 and tweet.lang == "en" and text_leng >=15):
                tweetBag.append(tweet.full_text)
            else:
                tweetBag.append("")
            
    except Exception as e:
        print("Error during API call: %s" % e)

# function to analize the sentiment of the text
def sentiment_analysis(text):
    response = openai.Completion.create(
        
        engine="text-davinci-003", # The name of the OpenAI language model to use for the analysis
         
        # prompt intializes the text that needs to be analyzed.
        prompt=f"What is the sentiment of the following text? Answer with either 'Positive' or 'Negative': {text}",

        max_tokens=1024, # used for both the prompt and generated text

        # n: The number of completions to generate for the prompt. In this case, it's set to 1,
        #  which means that only one sentiment score will be generated.
        n=1,

        # stop: the text will be read until the end of the sentence or unitl it reached max_tokens.
        stop=None,

        # Higher values like 0.8 will make the output more random, 
        # while lower values like 0.2 will make it more focused and deterministic.
        temperature=0.2,
    )

    #sentiment = response["choices"][0]["text"].strip() --> for one prompt
    #return sentiment

    if response.choices[0].text.strip() in ['Positive', 'Negative']:
        return response.choices[0].text.strip()
    else:
        return 'Unknown'

sentimentBug = [] # colleect the tweets in a bag

# Analyze each tweet 
for extractedTweet in tweetBag:
    sentimentBug.append(sentiment_analysis(extractedTweet));


positiveCount = 0; # count Positive sentiment
negativeCount = 0; # count Negative sentiment

# Count the number of positive and negative sentiment
positiveCount = sentimentBug.count("Positive")
negativeCount = sentimentBug.count("Negative")

# Create a dataframe of the sentiment values for visualization
df = pd.DataFrame({'sentiment': ['Positive', 'Negative'], 'count': [positiveCount, negativeCount]})

# visualize using seaborn
ax = sns.barplot(y='count', x='sentiment', hue='sentiment', data=df, palette={'Positive': 'green', 'Negative': 'red'})

# graph legend
legend = ax.legend()
legend.texts[0].set_text('Bullish')
legend.texts[1].set_text('Bearish') 

'''
    use this for testing purpose:

    # sentiment = sentiment_analysis(tweetBag[0])
    # print(tweetBag[0])
    # print("Sentiment:", sentiment)
'''

