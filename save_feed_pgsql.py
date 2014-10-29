# -*- coding: utf-8 -*-
import tweepy
from config.credentials import get_auth_credentials
from utils.pg_utils import PgPersistence
from config.credentials import get_auth_credentials
import time
from datetime import datetime

class CustomStreamListener(tweepy.StreamListener):
    """Guarda el stream en postgres.

    @param pg_persistence PgPersistence maneja la conección a la BD.
    """
    def __init__(self, pg_persistence, api=None ):
        super(CustomStreamListener,self).__init__()
        self.pg = pg_persistence

    def coordinates_formater(self,coords_json):
        """Regresa una tupla (long,lat)."""

        latitude = coords_json["coordinates"][1]
        longitude = coords_json["coordinates"][0]
        return (longitude,latitude)

    def date_formatter(self,date_string):
        """Regresa un objeto datetime"""
        print date_string
        dt = datetime.fromtimestamp(time.mktime(time.strptime(str(date_string),
                                                '%Y-%m-%d %H:%M:%S')))
        print str(dt)
        return dt

    def on_status(self, status):

        if status.coordinates is not None:
            print status.author.screen_name, status.created_at, status.text
            coordinates = self.coordinates_formater(status.coordinates)
            print coordinates
            date = self.date_formatter(status.created_at)
            row = [status.author.screen_name, status.text, date.date(),
                    date.time(), coordinates]
            self.pg.insert_row(row)


    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream


def start_stream(pg):
    while True:
        try:
            streamingAPI = tweepy.streaming.Stream(auth, CustomStreamListener(pg,api))
            streamingAPI.filter(locations=[-99.5,18.9,-98.5,20])
        except:
            time.sleep(60)
            continue

auth_dict = get_auth_credentials()
#use variables to access twitter
auth = tweepy.OAuthHandler(auth_dict["tw_consumer_key"], auth_dict["tw_consumer_secret"])
auth.set_access_token(auth_dict["tw_access_key"], auth_dict["tw_access_secret"])
api = tweepy.API(auth)
pg = PgPersistence(auth_dict)
start_stream(pg)
# streamingAPI = tweepy.streaming.Stream(auth, CustomStreamListener(pg,api))
# streamingAPI.filter(locations=[-99.5,18.9,-98.5,20])
