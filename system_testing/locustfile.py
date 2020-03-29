# locust --host=http://localhost:5000/v1/api --locustfile locust_posting.py

from locust import HttpLocust, TaskSet, task
import json
import random
from testinfo import *

class UserBehavior(TaskSet):

    #*********************************USERS*********************************
    @task(10)
    def create_account(self):
         if len(USER_CREDENTIALS) > 0:
            tuple = USER_CREDENTIALS.pop()
            ACTIVE_USERS.add(tuple[1],)
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            self.client.post("/user/register",data= {
              "email":tuple[0],
              "username":tuple[1],
              "password":tuple[2],
              "karma":tuple[3]
            },
            headers=headers,
            name = "Create new user")

    @task(5)
    def deactivate_acc(self):
        if (len(ACTIVE_USERS) > 0):
            username = random.sample(ACTIVE_USERS,1)[0]
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            self.client.delete("/user/deactivate_acc/"+str(username),
            headers=headers,
            name = "Deactivate account")

    @task(5)
    def decrement_karma(self):
        if (len(ACTIVE_USERS) > 0):
            username = random.sample(ACTIVE_USERS,1)
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            self.client.put("/user/sub_karma",data= {
              "username":username
            },
            headers=headers,
            name = "Decrement karma")

    @task(5)
    def increment_karma(self):
        if (len(ACTIVE_USERS) > 0):
            username = random.sample(ACTIVE_USERS,1)
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            self.client.put("/user/add_karma",data= {
              "username":username
            },
            headers=headers,
            name = "Increment karma")


    @task(5)
    def update_email(self):
        if (len(ACTIVE_USERS) > 0):
            username = random.sample(ACTIVE_USERS,1)
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            self.client.put("/user/update_email",data= {
              "username":username,
              "email":str(username)+"EmailChanged"
            },
            headers=headers,
            name = "Update email")


    #*********************************POSTING*********************************
    @task(10)
    def create_post(self):
            if (len(ACTIVE_USERS) > 0):
                username = random.sample(ACTIVE_USERS,1)
                posts = POSTS.pop()
                SUBREDDIT.add(posts[2],)
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            self.client.post("/posts/make_post",data= {
              "title":posts[0],
              "text":posts[1],
              "subreddit":posts[2],
              "username":username
            },
            headers=headers,
            name = "Create new post")

    @task(2)
    def delete_post(self):
        if (len(SUBREDDIT)>0):
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            self.client.delete("/posts/remove_post/"+str(len(SUBREDDIT)/2+1),
            headers=headers,
            name = "Delete post")

    @task(4)
    def list_all_posts(self):
        self.client.get("/posts/list_all_posts", name = "List all posts")

    @task(4)
    def list_sub_post(self):
        if (len(SUBREDDIT)>0):
            sub = random.sample(SUBREDDIT,1)[0]
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            self.client.get("/posts/list_post_sub/"+str(sub),
            headers=headers,
            name = "List subreddit posts")

    @task(2)
    def retrieve_post(self):
        if (len(SUBREDDIT)>0):
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            self.client.get("/posts/retrieve_post/"+str(len(SUBREDDIT)/2+1),
            headers=headers,
            name = "Retrieve post")


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 60000
