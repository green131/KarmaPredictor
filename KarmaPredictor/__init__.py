import time
import datetime
import praw
import random

global numPosts
global rnd

def convertCreated(integer):
    created = time.gmtime(integer)
    return created

def optimize(r, opLimit):
    av = [0, 0, 0.0]
    i=0
    for submission in r.get_front_page(limit=opLimit):
        #Submission Variables
        created = submission.created_utc
        ups = submission.ups
        downs = submission.downs
        #Calculate Aditional Parameters
        ratio = getRatio(ups, downs)
        gap = getTimeDifference(created)
        #DEBUG
        #print("hours: " + str(gap) + " PPH: " + str(score / gap) + " ratio: " + str(ratio))
        #Increment Variables
        av[0]+=1
        av[1]+=gap
        av[2]+=ratio
        #Percent Counter
        i+=1
        if i%(int(opLimit/10)) == 0:
            print(str(int((i/opLimit)*100)) + "%")
    #Calculate Averages for All Values
    av[1] = av[1] / av[0]
    av[2] = av[2] / av[0]
    #Determine gap in time
    av[1]*=0.3
    return av[1:]
        
def getRatio(up, down):
    #Up to down ratio
    if down == 0: ratio = up
    else: ratio = float(up) / float(down)
    return ratio

def getTimeDifference(created):
    #Get how old post is (hours)
    tb = convertCreated(time.time() - created)
    tb_day = tb[2]
    tb_hour = tb[3]
    gap = ((tb_day - 1) * 24) + tb_hour
    if gap < 1: gap = 1
    return gap

def getLikely(dt, up, down, comms):
    if down < 1: down = 1
    if dt < 1: dt = 1
    if comms < 1: comms = 1
    return float(1.0/float(dt)) * float(float(up)/(float(down) * 3.0)) * (20.0 / float(comms))
    
def testSubmission(submission, av):
    #Submission Variables
    sid = submission.id
    permalink = submission.permalink
    created = submission.created_utc
    score = submission.score
    ups = submission.ups
    downs = submission.downs
    num_comments = submission.num_comments
    #Determine time between post and current time
    dt = getTimeDifference(created)
    #Compare how old post is, points per hour, and ratio of upvotes to downvotes
    if ((dt) < av[0]) & (int(getRatio(ups, downs)) > av[1]):
        likely = int(getLikely(dt, ups, downs, num_comments))
        if likely > 0:
            print(" FOUND {\n" +
                "  LIKELY: " + str(likely) + "\n" +
                "  ID: " + str(sid) + "\n" +
                "  SCORE: " + str(score) + "\n" +
                "  COMMENTS: " + str(num_comments) + "\n" +
                "  LINK: " + str(permalink) + "\n" +
                "  Posted " + str(dt) + " hour(s)" + " ago.\n" +
                " }"
            )
            doc = open('C:/Users/Daniel/Documents/GitHub/KarmaPredictor/KarmaPredictor/Base/links'+str(rnd)+'.txt', 'a')
            doc.write("[" + str(likely) + "]\t\t" + str(permalink) + "\n")
            doc.close()
            return True
    return False

def findProspective(r, found, numPosts, startingPostLimit, av):
    #Exceeded specs
    if (numPosts > 2000):
        print("Limit Exceeded. Stopping...")
        return
    i=0.0
    for submission in r.get_front_page(limit=numPosts):
        i+=1
        #If posts have already been covered, skip
        if (int(numPosts/2) > i) & (startingPostLimit != numPosts): pass
        elif testSubmission(submission, av): found+=1
        #Percent Counter
        if i%(numPosts/10) == 0:
            print(str(int((i/numPosts)*100)) + "%")
    #If very few found, search wider specs
    if (found < 5):
        numPosts*=2
        av[0]*=1.2
        print("Expanding Search... [posts:" + str(numPosts) + "]")
        findProspective(r, found, numPosts, startingPostLimit, av)

#-------------------Main Script-------------------------
rnd = 0
found = 0
opLimit = 40.0
numPosts = 1000.0
startingPostLimit = 1000.0
if __name__ == "__main__":
    #Create Record Text File
    rnd = random.randrange(10000, 99999, 1)
    print("Recording Results to links" + str(rnd) + ".txt")
    #Login & Connection
    r = praw.Reddit(user_agent="github/green131/karmapredictor")
    r.login()
    print("Opimizing Scan...")
    av = optimize(r, opLimit)
    print("...Opimization Complete")
    print("Beginning Scan...")
    #Find Up and Coming Submissions
    findProspective(r, found, numPosts, startingPostLimit, av)
    print("...Scan Complete")
        