#Create a new post
curl -d 'title=TestPost1&text=TestText1&subreddit=TestSub1&username=TestUsername' http://localhost:5000/v1/api/posts/make_post

#Retrieve an existing post
curl --request GET "http://localhost:5000/v1/api/posts/retrieve_post/1"

#List the n most recent posts to any community
curl --request GET "http://localhost:5000/v1/api/posts/list_all_posts/"

#List the n most recent posts to a particular community
curl --request GET "http://localhost:5000/v1/api/posts/list_post_sub/TestSub1/"

#Delete an existing post
curl -X DELETE 'http://localhost:5000/v1/api/posts/remove_post/1'
