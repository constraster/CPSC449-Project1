USER_CREDENTIALS = set()
ACTIVE_USERS=set()
POSTS=set()
SUBREDDIT=set()
for i in range(1,200):
    USER_CREDENTIALS.add(("TestEmail"+str(i),"TestUsername"+str(i), "TestPassword"+str(i), 0))
    POSTS.add(("TestTitle"+str(i),"TestBody"+str(i),"TestSub"+str(i)))
