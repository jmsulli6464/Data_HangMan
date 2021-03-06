import os
# Import the necessary package to process data in JSON format
import tweepy #https://github.com/tweepy/tweepy
import csv

def twitter(screen_name):
    consumer_key = str(os.environ.get("CONSUMER_KEY"))
    consumer_secret = str(os.environ.get("CONSUMER_SECRET"))
    access_token = str(os.environ.get("ACCESS_TOKEN"))
    access_secret = str(os.environ.get("ACCESS_SECRET"))

    #Twitter only allows access to a users most recent 3240 tweets with this method

    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)

    #initialize a list to hold all the tweepy Tweets
    alltweets = []

    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)

    #save most recent tweets
    alltweets.extend(new_tweets)

    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:

    	#all subsiquent requests use the max_id param to prevent duplicates
    	new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)

    	#save most recent tweets
    	alltweets.extend(new_tweets)

    	#update the id of the oldest tweet less one
    	oldest = alltweets[-1].id - 1

    	print ((len(alltweets)))

    #transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]

    #write the csv
    with open('tweets.csv', 'w') as f:
    	writer = csv.writer(f)
    	writer.writerow(["id","created_at","text"])
    	writer.writerows(outtweets)

    pass

def main():

    twitter('') #Insert username here you want to download


if __name__ == '__main__':
    main()
