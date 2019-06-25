#!/usr/bin/python
import praw
import pdb
import re
import os
import mysql.connector as mysql
import datetime

def main():

    #create instance of reddit
    reddit = praw.Reddit('bot1')

    #subreddit to monitor is r/Jokes
    subreddit = reddit.subreddit("jokes")

    #lopp through all new submissions 
    for submission in subreddit.stream.submissions():
        process_joke(submission)
    
#extract text from joke submission and reply to submission according to whether the joke is new or not
def process_joke(submission):
    normalized_title = submission.title.lower()
    normalized_text = submission.selftext.lower()
    user = submission.author
    joke = normalized_title + " " + normalized_text
    date = datetime.datetime.fromtimestamp(submission.created)

    output = jokeIsNew(str(user),str(joke),str(date))
    newJoke = output[0]
    
    if newJoke:
        submission.reply("Wow, original content for once. Carry on, redditzen." + "\n\n  *****" + "\n\n  ^I ^am ^a ^bot ^under ^training. ^Tracking ^of ^jokes ^started ^6/24/2019. ^Open ^to ^feedback.")
    else:
        ogDate = datetime.datetime.strptime(output[1], "%Y-%m-%d %H:%M:%S")
        daysSinceRepost = str(date-ogDate)
        submission.reply("This is the Joke Repost Police and you have been arrested for reposted content. This joke was posted " + daysSinceRepost + " ago " + "by u/" + output[2] + "\n\n  *****" + "\n\n  ^I ^am ^a ^bot ^under ^training. ^Tracking ^of ^jokes ^started ^6/24/2019. ^Open ^to ^feedback.")

#compare the joke submission text to jokes already within the database
#return [True, 0, 0] if new and add joke to database 
#return [False, date of original joke, author of original joke] if reposted 
def jokeIsNew(user, joke, date):
    
    db = mysql.connect(
        host = "localhost",
        user = "root",
        password = "password",
        auth_plugin='mysql_native_password',
        database = 'jokes'
        )       

    cursor = db.cursor()   
    output = [True, 0, 0]

    cursor.execute("SELECT * FROM joke_submissions")
    for entry in cursor:
        if joke == entry[2]:
            output[0] = False
            output[1] = entry[3]
            output[2] = entry[1]
    if output[0]:
        sql = "INSERT INTO joke_submissions (userID, joke_text, dateOfEntry) VALUES (%s, %s, %s)"
        val = (user,joke,date)
        cursor.execute(sql,val)
        db.commit() 
    
    return output


if __name__ == "__main__":
    main()