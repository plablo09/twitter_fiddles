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
    """En esta versión no recibimos palabras clave.

    Para darle la vuelta al problema de la actualización de las filas, creamos
    un nuevo worksheet vacio y usamos append_row() siempre
    """
    def __init__(self, credentials,worksheet, api=None ):
        super(CustomStreamListener,self).__init__()
        #self.row_number = 448
        self.wks = worksheet
        #gc = gspread.login(auth_dict['google_uname'], auth_dict['google_pwd'])
        #self.wks = gc.open('DilmaNovamente_2').sheet1

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


        if status.coordinates is not None:
            print status.coordinates
            print status.author.screen_name, status.created_at, status.text
            coordinates = self.coordinates_formater(status.coordinates)
            print coordinates
            row = (status.author.screen_name,status.created_at,status.text,
                    coordinates[0], coordinates[1])
            self.wks.append_row(row)


    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream


def start_stream(worksheet):
    while True:
        try:
            streamingAPI = tweepy.streaming.Stream(auth, CustomStreamListener(auth_dict,worksheet))
            streamingAPI.filter(locations=[-99.5,18.9,-98.5,20])
        except:
            continue

gc = gspread.login(auth_dict['google_uname'], auth_dict['google_pwd'])
try:
    sh = gc.open('store_stream')
except HTTPError as e:
    print(e)
#tenemos que ver si ya existe el wks de trabajo, para no escribir miles
if len(sh.worksheets()) >1:
    wks = sh.get_worksheet(1)
else:
    wks = sh.add_worksheet(title="stream",rows="1",cols="10")

start_stream(wks)

# streamingAPI = tweepy.streaming.Stream(auth, CustomStreamListener(auth_dict,'DilmaNovamente'))
# #streamingAPI.filter(track=['LaVerdaderaPruebaDeAmorConsisteEn'])-180,-90,180,90
# streamingAPI.filter(locations=[-180,-90,180,90])
# #streamingAPI.filter(locations=[-115,12,-87,33])
