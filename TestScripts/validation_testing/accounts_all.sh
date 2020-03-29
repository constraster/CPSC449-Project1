#Create user
curl -d 'email=TestEmail&username=TestUsername&password=Test&karma=0' http://localhost:5000/v1/api/user/register

#Decrement Karma
curl -X PUT -d 'username=TestUsername' http://localhost:5000/v1/api/user/sub_karma

#Increment Karma
curl -X PUT -d 'username=TestUsername' http://localhost:5000/v1/api/user/add_karma

#Update email
curl -X PUT -d 'username=TestUsername&email=TestEmailChanged' http://localhost:5000/v1/api/user/update_email

#Deactivate account
curl -X DELETE 'http://localhost:5000/v1/api/user/deactivate_acc/TestUsername'
