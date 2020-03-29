USER_CREDENTIALS = set(("TestUsername", "TestEmail", "TestPassword", 0))
ACTIVE_USERS=set()
POSTS=set(("TestTitle","TestBody","TestSub"))
SUBREDDIT=set()
for i in range(1,200):
    USER_CREDENTIALS.add(("TestEmail"+str(i),"TestUsername"+str(i), "TestPassword"+str(i), 0))
    POSTS.add(("TestTitle"+str(i),"TestBody"+str(i),"TestSub"+str(i)))
