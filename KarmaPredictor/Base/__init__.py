import time
import datetime
import praw
import math

global numPosts

def convertCreated(integer):
    created = time.gmtime(integer)
    return created

def hasKeyword(string, keywords):
    return any(word in string for word in keywords)

def testSubmission(submission):
    #Submission Variables
    sid = submission.id
    sub = submission.subreddit.name
    permalink = submission.permalink
    created = submission.created_utc
    score = submission.score
    ups = submission.ups
    downs = submission.downs
    num_comments = submission.num_comments
    #Determine time between post and current time
    tb = convertCreated(time.time() - created)
    tb_day = tb[2]
    tb_hour = tb[3]
    #How old post is (hours)
    gap = ((tb_day - 1) * 24) + tb_hour
    if gap < 1: gap = 1
    #Up to down ratio
    if downs == 0: 
        ratio = ups
    else: 
        ratio = ups / downs
    #If post is <3 hrs old, points per hour > 200, and up:down >= 3:1
    if (gap) <= 3 & int(score / gap) > 200 & int(ratio) >= 3:
        print(" FOUND {\n" +
            "  ID: " + str(sid) + "\n" +
            "  SubReddit: " + str(sub) + "\n" +
            "  SCORE: " + str(score) + "\n" +
            "  COMMENTS: " + str(num_comments) + "\n" +
            "  LINK: " + str(permalink) + "\n" +
            "  Posted " + str(gap) + " hour(s)" + " ago.\n" +
            " }"
        )
        doc = open('links.txt', 'a')
        if submission.id not in doc:
            doc.append(str(permalink))
        doc.close()
        return True
    return False

def findProspective(r, numPosts, startingPostLimit):
    #Exceeded specs
    if (numPosts > 2000):
        return
    i=0.0
    found=0
    for submission in r.get_front_page(limit=numPosts):
        i+=1
        if (int(numPosts/2) > i) & (startingPostLimit != numPosts):
            pass
        else:
            if testSubmission(submission): found+=1
        #Percent Counter
        if i%(numPosts/10) == 0:
            print(str(int((i/numPosts)*100)) + "%")
    #If very few found, search wider specs
    if (found < 5):
        numPosts*=2
        print("Expanding Search... [posts:" + str(numPosts) + "]")
        findProspective(r, numPosts, startingPostLimit)

#-------------------Main Script-------------------------
sleep = 60
max_searching = 15
numPosts = 500.0
startingPostLimit = 500.0
reqComments = 100
if __name__ == "__main__":
    #Login & Connection
    r = praw.Reddit(user_agent="github/green131/karmapredictor")
    r.login()
    keywords = [] #Keywords to check for
    print("Beginning Scan...")
    #Find Up and Coming Submissions
    findProspective(r, numPosts, startingPostLimit)
    print("...Scan Complete")
