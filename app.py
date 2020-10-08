import tweepy
import time
import pandas as pd
import random
import numpy as np
import io
from keys import keys


# plug your twitter API Keys into the key folder
CONSUMER_KEY = keys['CONSUMER_KEY']
CONSUMER_SECRET = keys['CONSUMER_SECRET']
ACCESS_KEY = keys['ACCESS_KEY']
ACCESS_SECRETE = keys['ACCESS_SECRETE']


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRETE)
# connect to twitter API
api = tweepy.API(auth)

# load the excel data to python 
smpd = pd.read_excel("sampleData.xlsx", sheet_name="shitOne")

# check your id file for the tweet id 
# if the tweet is there then retrun True otherwise return False
def checkId(id):
    with open("ids.txt") as openfile:
        for line in openfile:
            for part in line.split():
                # if the id exists among the lines
                if id in part:
                    return True
                    break
                # else if the id doe not exist among the lines

    return False

# record the id in the text file
def writeId(id):
    f = open("ids.txt", "a")
    f.write(id + "\n")
    f.close()

# search for tweets with hastags and reply to it using one of the cells in excel file
def replyToTweets():
    # your custom hashtag
    search1 = "#botysha3ir"
    # your custom hashtag
    search2 = "#boty7akim"
    # number of tweets to check every time a search is performed
    nTweets = 10

    # search for the tweet with  the first custom hashtag
    for tweet in tweepy.Cursor(api.search, search1).items(nTweets):
        #if the tweet id is not in the ids.txt folder 
        if(checkId(str(tweet.id)) == False):
            # record the id in the text file
            writeId(str(tweet.id))
            # select a cell number from  the excel file randomly 
            randVal = random.randint(0, len(smpd["poem"]))
            # get the user's  name
            sn = tweet.user.screen_name
            # put the cell data into a string
            content = str(smpd["poem"][randVal])
            # create a custom string and combine the cell data with the user's name add any other thing you like 
            m = "@%s '%s' \n #Automatically_Replied 🙂" % (sn, content)
            api.update_status(m, tweet.id)
            # tweet.favorite()
            time.sleep(5)

    # search for the tweet with  the second custom hashtag
    # same as the fist one
    for tweet in tweepy.Cursor(api.search, search2).items(nTweets):

        if(checkId(str(tweet.id)) == False):
            writeId(str(tweet.id))
            randVal = random.randint(0, len(smpd["quote"]))
            sn = tweet.user.screen_name
            content = str(smpd["quote"][randVal])
            m = "@%s '%s' \n #Automatically_Replied 🙂" % (sn, content)
            api.update_status(m, tweet.id)
            # tweet.favorite()
            time.sleep(5)

# for ever check for new tweets every 15 seconds
while(True):
    replyToTweets()
    time.sleep(15)
