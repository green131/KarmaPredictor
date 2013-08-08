import time
import datetime
import praw

global numPosts

def convertCreated(integer):
    created = time.gmtime(integer)
    return created

def hasKeyword(string, keywords):
    return any(word in string for word in keywords)

def testSubmission(submission):
    #Submission Variables
    sid = submission.id
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
    #If post is < 3 hrs old, points per hour > 100, and up:down >= 3:1
    if (gap) <= 5 & int(score / gap) > 200 & int(ratio) >= 3:
        print(" FOUND {\n" +
            "  ID: " + str(sid) + "\n" +
            "  SCORE: " + str(score) + "\n" +
            "  COMMENTS: " + str(num_comments) + "\n" +
            "  LINK: " + str(permalink) + "\n" +
            "  Posted " + str(gap) + " hour(s)" + " ago.\n" +
            " }"
        )
        doc = open('C:/Users/Daniel/Documents/GitHub/KarmaPredictor/KarmaPredictor/Base/links.txt', 'a')
        #if str(permalink) not in doc:
        doc.write(str(permalink) + "\n")
        doc.close()
        return True
    return False

def findProspective(r, found, numPosts, startingPostLimit):
    #Exceeded specs
    if (numPosts > 2000):
        print("Limit Exceeded. Stopping...")
        return
    i=0.0
    for submission in r.get_front_page(limit=numPosts):
        i+=1
        #If posts have already been covered, skip
        if (int(numPosts/2) > i) & (startingPostLimit != numPosts): pass
        elif testSubmission(submission): found+=1
        #Percent Counter
        if i%(numPosts/10) == 0:
            print(str(int((i/numPosts)*100)) + "%")
    #If very few found, search wider specs
    if (found < 5):
        numPosts*=2
        print("Expanding Search... [posts:" + str(numPosts) + "]")
        findProspective(r, found, numPosts, startingPostLimit)

#-------------------Main Script-------------------------
found = 0
sleep = 60
numPosts = 50.0
startingPostLimit = 50.0
reqComments = 100
if __name__ == "__main__":
    #Login & Connection
    r = praw.Reddit(user_agent="github/green131/karmapredictor")
    r.login()
    keywords = [] #Keywords to check for
    print("Beginning Scan...")
    #Find Up and Coming Submissions
    findProspective(r, found, numPosts, startingPostLimit)
    print("...Scan Complete")
