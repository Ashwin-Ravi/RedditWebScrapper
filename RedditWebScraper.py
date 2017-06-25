#Python Version: 2.7
#Instructions to Execute:
#make sure BeautifulSoup4, praw, nltk has been installed before running the program
#if not, install using the pip install commands (Example : 'pip install BeautifulSoup4')

#Importing necessary libraries
from urllib2 import Request, urlopen
import urllib2
from time import sleep
from bs4 import BeautifulSoup
import praw
from praw.models import MoreComments
import thread
from multiprocessing.pool import ThreadPool
import nltk
from nltk.corpus import stopwords
import collections
nltk.download('stopwords')


#Function to read data from an url and return data
def urlRead(requested):
    try:
        response = urlopen(requested)
        data = response.read()
    except:
        sleep(7)
        response = urlopen(requested)
        data = response.read()
    return data


#Defining url and headers
headers = {'User-agent':'WeekendProject'}
URL = 'https://www.reddit.com/r/all/'

#Requesting data from the url
request = Request(URL, None, headers)
data = urlRead(request)

#Filtering out only posts from the data using BeautifulSoup
#Filters out data of class = "first" - class of posts
soup = BeautifulSoup(data, 'html.parser')
commentLinks = soup.find_all("li", class_="first")

#Filtering details of Top 10 posts
topTitles = soup.find_all("a", class_=["title may-blank ", "title may-blank outbound"])[:10]

#saving Comment url of each post for future use
seed = 'https://www.reddit.com'
commentLinkList = []
for eachObject in commentLinks:
    links = eachObject.find("a", class_="bylink comments may-blank")
    if (links.get('href'))[0:4]=='http':
        currentLink = (links.get('href'))
    else:
        currentLink = seed + (links.get('href')) #internal reddit links will not have beginning part of the link(seed)
    commentLinkList.append(currentLink)
    

#**************************************************************************************************************

#Function to return - Top comments and Top Keywords of the subreddit link.
def getCommentsAndKeywords(commentLinkComment):
    
    #Using python Reddit API Wrapper (praw) to retrieve comments from
    #//using praw due to its efficiency and ease of use//
    #Defining user details to access reddit using praw
    myuser_agent = 'Comment Extraction by /u weekendProject'
    myclient_secret = 'Enter Your client_secret'
    myusername = 'Enter Your username'
    mypassword = 'Enter Your password'
    myclient_id = 'Enter Your client ID'
    reddit = praw.Reddit(user_agent = myuser_agent,
                         client_id = myclient_id, client_secret = myclient_secret,
                         username = myusername, password = mypassword)

    #Retrieve comments from url
    submission = reddit.submission(url = commentLinkComment)

    #Replaces/Removes "More comments" from the data obtained
    submission.comments.replace_more(limit=0)

    #Storing Comment body and points in dictionary
    commentDict = {}
    for comment in submission.comments.list():
        commentDict[comment.body] = comment.score

    #Sorting and obtaining the top 10 comments by points
    TopComments = (sorted(commentDict, key=commentDict.__getitem__, reverse=True))[:10]

    #Obtaining whole comment text
    commentFull=''
    for comment in submission.comments.list():
        commentFull = commentFull + '\n' + comment.body
    commentFull = commentFull.lower()
    
    #Removing the most frequent english words ex: 'the', 'a', 'an'
    s=set(stopwords.words('english'))
    token1 = filter(lambda word: not word in s,commentFull.split())

    #counting and extracting top 10 key words
    counter = collections.Counter(token1)
    topWords = ((counter.most_common())[:10])
    return (TopComments, topWords)


#Using MultiThreading to obtaing Top 10 comment and keywords
pool = ThreadPool(processes=1)
Thread = []
for j in range(0,10):
    Thread.append(pool.apply_async(getCommentsAndKeywords, (commentLinkList[j], )))


#Getting results from all threads
Thread_result = []
for j in range(0,10):
    Thread_result.append(Thread[j].get())


#Printing the results
rank = 0
for item in topTitles:
    rank=rank+1
    print "Item No.: " + str(rank)
    print item.text
    if (item.get('href'))[0:4]=='http':
        print "url: " + (item.get('href'))
    else:
        print "url: " + seed + (item.get('href'))
    print "Comment url: " + commentLinkList[rank-1]

    print "Top Comments: "
    for i in range(0,10):
        print str(i+1) + ': ',
        print ((Thread_result[rank-1])[0])[i]
    print "Top Key Words: "
    for i in range(0,10):
        print (((Thread_result[rank-1])[1])[i])[0],
        print ', ',
    print '\n'
