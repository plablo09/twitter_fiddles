# -*- coding: utf-8 -*-
import sys
import json
import gspread
import tweepy
from config.credentials import get_auth_credentials

auth_dict = get_auth_credentials()
#use variables to access twitter
auth = tweepy.OAuthHandler(auth_dict["tw_consumer_key"], auth_dict["tw_consumer_secret"])
auth.set_access_token(auth_dict["tw_access_key"], auth_dict["tw_access_secret"])
api = tweepy.API(auth)


#create an object called 'customStreamListener'
class CustomStreamListener(tweepy.StreamListener):
    """Esta versión recibe una palabra clave y filtra el stream.

    Para actualizar el renglón del google spread en el que se escribe, lleva la
    cuenta en row_number. El problema es que cuando el script se reinicia se
    pierde la cuenta
    """

    def __init__(self, credentials, keyword,api=None, ):
        super(CustomStreamListener,self).__init__()
        self.row_number = 448
        self.keyword = keyword
        gc = gspread.login(auth_dict['google_uname'], auth_dict['google_pwd'])
        self.wks = gc.open('DilmaNovamente_2').sheet1

    def write_row(self,row, row_number):
        self.wks.update_cell(row_number, 1, row[0])
        self.wks.update_cell(row_number, 2, row[1])
        self.wks.update_cell(row_number, 3, row[2])
        self.wks.update_cell(row_number, 4, row[3])
        self.wks.update_cell(row_number, 5, row[4])

    def coordinates_formater(self,coords_json):
        latitude = coords_json["coordinates"][1]
        longitude = coords_json["coordinates"][0]
        return (longitude,latitude)


    def on_status(self, status):

        if self.keyword.lower() in status.text.lower():
            if status.coordinates is not None:
                print status.coordinates
                print status.author.screen_name, status.created_at, status.text
                coordinates = self.coordinates_formater(status.coordinates)
                print coordinates
                row = (status.author.screen_name,status.created_at,status.text,
                        coordinates[0], coordinates[1])
                self.write_row(row, self.row_number)
                self.row_number += 1 #move to the next row


    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream


def start_stream():
    while True:
        try:
            streamingAPI = tweepy.streaming.Stream(auth, CustomStreamListener(auth_dict,'DilmaNovamente'))
            streamingAPI.filter(locations=[-180,-90,180,90])
        except:
            continue

start_stream()

# streamingAPI = tweepy.streaming.Stream(auth, CustomStreamListener(auth_dict,'DilmaNovamente'))
# #streamingAPI.filter(track=['LaVerdaderaPruebaDeAmorConsisteEn'])-180,-90,180,90
# streamingAPI.filter(locations=[-180,-90,180,90])
# #streamingAPI.filter(locations=[-115,12,-87,33])
