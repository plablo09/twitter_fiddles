# -*- coding: utf-8 -*-

import sys
from TwitterSearch import *
#
# auth_dict = get_auth_credentials()
# #use variables to access twitter
# auth = tweepy.OAuthHandler(auth_dict["tw_consumer_key"],
#                             auth_dict["tw_consumer_secret"])
# auth.set_access_token(auth_dict["tw_access_key"], auth_dict["tw_access_secret"])
# api = tweepy.API(auth)
def search_twitter(credentials,keywords):
    """Performs a search against the twitter search API.

        @param dict credentials     The auth credentials
        @param list keywords        The list of nkeywords to search

        @returns TwitterSearch.searchTweetsIterable()   The search results

    """

    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.setKeywords(keywords) # let's define all words we would like to have a look for
    #tso.setLanguage('de') # we want to see German tweets only
    tso.setCount(7) # please dear Mr Twitter, only give us 7 results per page
    tso.setIncludeEntities(False) # and don't give us all those entity information
    print tso.createSearchURL()
    # it's about time to create a TwitterSearch object with our secret tokens
    ts = TwitterSearch(
        consumer_key = credentials["tw_consumer_key"],
        consumer_secret = credentials["tw_consumer_secret"],
        access_token = credentials["tw_access_key"],
        access_token_secret = credentials["tw_access_secret"]
     )

    # for tweet in ts.searchTweetsIterable(tso):
    #     print( '@%s tweeted: %s' % ( tweet['user']['screen_name'], tweet['text'] ) )
    return ts.searchTweetsIterable(tso)
