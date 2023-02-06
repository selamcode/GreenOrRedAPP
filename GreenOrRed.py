
# openAi api key --> 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

import tweepy
import openai

# Your openAi API credentials
openai.api_key = "openai api key"



# Your Twitter API credentials
consumer_key = "consumer_key"
consumer_secret = "consumer_secret"
access_token = "access_token"
access_token_secret = "access_token_secret"

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
       
        tweets = api.search_tweets(KEYWORDS, result_type="recent", count=100, tweet_mode="extended")
        
        
        #tweets = api.search_tweets(KEYWORDS, result_type="popular", tweet_mode="extended")
        #tweets = api.search_tweets(KEYWORDS, result_type="mixed", tweet_mode="extended")

        for tweet in tweets:
            text_leng = len(tweet.full_text.split())
            if (not tweet.retweeted and tweet.user.followers_count >= 500 and tweet.lang == "en" and text_leng >=15):
                tweetBag.append(tweet.full_text)
            

    except Exception as e:
        print("Error during API call: %s" % e)
print(tweetBag[0])


def sentiment_analysis(text):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"What is the sentiment of the following text, answer Positive or Negative: {text}",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    sentiment = response["choices"][0]["text"].strip()
    return sentiment


sentiment = sentiment_analysis(tweetBag[0])
print("Sentiment:", sentiment)