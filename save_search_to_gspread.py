from config.credentials import get_auth_credentials
from utils.search_twitter import search_twitter
from TwitterSearch import TwitterSearchException
import gspread


auth_dict = get_auth_credentials()
gc = gspread.login(auth_dict['google_uname'], auth_dict['google_pwd'])
wks = gc.open('DilmaNovamente_3').sheet1
def write_row(row, row_number):
    wks.update_cell(row_number, 1, row[0])
    wks.update_cell(row_number, 2, row[1])
    wks.update_cell(row_number, 3, row[2])
    wks.update_cell(row_number, 4, row[3])
    wks.update_cell(row_number, 5, row[4])

def coordinates_formater(coords_json):
    latitude = coords_json["coordinates"][1]
    longitude = coords_json["coordinates"][0]
    return (longitude,latitude)

try:
    search_iterable = search_twitter(auth_dict,['DilmaNovamente'])
    row_number = 2
    for tweet in search_iterable: # this is where the fun actually starts :)
        if tweet['coordinates'] is not None:
            coords = coordinates_formater(tweet['coordinates'])
            row = (tweet['user']['screen_name'],
                    tweet['created_at'], tweet['text'],coords[1],coords[0])
            write_row(row, row_number)
            print( '@%s tweeted: %s on location: %s' % ( tweet['user']['screen_name'],
                    tweet['text'], tweet['coordinates'] ) )
            row_number += 1

except TwitterSearchException as e: # take care of all those ugly errors if there are some
    print(e)
