import sys
import tweepy
import csv

#pass security information to variables
consumer_key = "13TegYgQ9F3FyShqB47LFsrM4"
consumer_secret = "zMOQluT6jUJj4xmZrEBoknzI6cHBEWIq2GvQbmLmUfpDG5q8pP"
access_key = "113179867-1XjAkP3BmB4NhvEWyYhFj3SDLTCdLQJClZQSpAgW"
access_secret = "30PVB8MFawR0cfkPfPDZKEBr6XZGkx3anEUHo5yDsPiyX"


#use variables to access twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

#create an object called 'customStreamListener'


class CustomStreamListener(tweepy.StreamListener):

    global writer
    writer = csv.writer(open('file.csv', 'w+'))
    writer.writerow(('Author', 'Date', 'Text'))

    def on_status(self, status):
        print status.author.screen_name, status.created_at, status.text
        writer.writerow((status.author.screen_name.encode('utf-8'), status.created_at, status.text.encode('utf-8')))

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream




streamingAPI = tweepy.streaming.Stream(auth, CustomStreamListener())
streamingAPI.filter(track=['Ayotzinapa'])
