#Create user
curl -d 'email=TestEmail&username=TestUsername&password=Test&karma=0' http://localhost:5000/v1/api/user/register

#Decrement Karma
curl -X PUT -d 'username=TestUsername' http://localhost:5000/v1/api/user/sub_karma

#Increment Karma
curl -X PUT -d 'username=TestUsername' http://localhost:5000/v1/api/user/add_karma

#Update email
curl -X PUT -d 'username=TestUsername&email=TestEmailChanged' http://localhost:5000/v1/api/user/update_email

#Create a new post
curl -d 'title=TestPost1&text=TestText1&subreddit=TestSub1&username=TestUsername' http://localhost:5000/v1/api/posts/make_post

#List the n most recent posts to any community
curl --request GET "http://localhost:5000/v1/api/posts/list_all_posts/"

#List the n most recent posts to a particular community
curl --request GET "http://localhost:5000/v1/api/posts/list_post_sub/TestSub1/"

#Retrieve an existing post
curl --request GET "http://localhost:5000/v1/api/posts/retrieve_post/1"

#Delete an existing post
curl -X DELETE 'http://localhost:5000/v1/api/posts/remove_post/1'

#Deactivate account
curl -X DELETE 'http://localhost:5000/v1/api/user/deactivate_acc/TestUsername'
