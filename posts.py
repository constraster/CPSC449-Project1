from datetime import datetime
import os
import pytz
from pytz import timezone
import request
from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime
from users import User

posts = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
posts.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'logs.db')
db = SQLAlchemy(posts)
mar = Marshmallow(posts)

def get_time():
    date = datetime.now(tz=pytz.utc)
    date = date.astimezone(timezone('US/Pacific'))
    pstTime = date
    return pstTime

# create a class for posts
# holds information for posts
class Post(db.Model):
    _table_name = 'post'
    postID = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    title = Column(String(120), nullable=False)
    text = Column(String(500), nullable=False)
    subreddit = Column(String(20), nullable=False)
    createtime = Column(DateTime, default=get_time())
    changetime = Column(DateTime, default=get_time())

    # this function is used to list out the variables without manually returning them all
    # just reference this function to output everything
    def serialize(self):
        return {
            "postID": self.postID,
            "username": self.username,
            "title": self.title,
            "text": self.text,
            "subreddit": self.subreddit,
            "createtime": self.createtime,
            "changetime": self.changetime
        }

# schema for posts
class PostData(mar.Schema):
    class Data:
        fields = ('id', 'username', 'title', 'text', 'subreddit', 'createtime', 'changetime')


postdata = PostData()
postmultdata = PostData(many=True)


@posts.cli.command('create_db')
def create_db():
    db.create_all()
    print('created a database')


@posts.cli.command('drop_db')
def drop_db():
    db.drop_all()
    print('dropped the db')


@posts.cli.command('seed_db')
def seed_db():
    post = Post(username='FrancisNguyen', title="CSUF goes virtual after coronavirus outbreak",
                text="Most of the classes will go on zoom", subreddit="CSUF")
    db.session.add(post)
    db.session.commit()
    print('DB seeded')

@posts.route('/')
def index():
    return 'Hello World'


# create a post
@posts.route('/v1/api/posts/make_post', methods=['POST'])
def make_post():
    username = request.form['username']
    makep = User.query.filter_by(username=username).first()
    if makep:
        username = request.form['username']
        title = request.form['title']
        text = request.form['text']
        subreddit = request.form['subreddit']
        createtime = get_time()
        changetime = get_time()
        post = Post(username=username, title=title, text=text, subreddit=subreddit,
                    createtime=createtime, changetime=changetime)
        db.session.add(post)
        db.session.commit()
        return jsonify(message='Post created'), 201
    else:
        return jsonify(message='Username does not exist'), 409


# delete a post
@posts.route('/v1/api/posts/remove_post/<int:pid>', methods=['DELETE'])
def delete_post(pid: int):
    post = Post.query.filter_by(postID=pid).first()
    if post:
        Post.query.filter_by(postID=pid).delete()
        db.session.commit()
        return jsonify(message="Deleted a post"), 202
    else:
        return jsonify(message="Post does not exist"), 404


# retrieve a post
@posts.route('/v1/api/posts/retrieve_post/<int:pid>', methods=['GET'])
def get_post(pid: int):
    post = Post.query.filter_by(postID=pid).first()
    if post:
        # references serialize() to list out all fields
        return jsonify(post.serialize())
    else:
        return jsonify(message="Post does not exist"), 404


# list posts by subreddit
@posts.route('/v1/api/posts/list_post_sub/<string:subreddit>/', methods=['GET'])
def list_post_sub(subreddit: str):
    # create amount argument to pass into the limit() function
    amount = request.args.get('amount')
    postssub = db.session.query(Post).filter_by(subreddit=subreddit).order_by(Post.createtime.desc()).limit(amount)
    if posts:
        # serializes every variable in posts and returns them
        return jsonify(posts=[i.serialize() for i in postssub])
    else:
        return jsonify(message="Post does not exist"), 404


# list all posts
@posts.route('/v1/api/posts/list_all_posts/', methods=['GET'])
def list_all_posts():
    # create amount argument to pass into the limit() function
    amount = request.args.get('amount')
    listposts = db.session.query(Post).order_by(Post.createtime.desc()).limit(amount)
    return jsonify(listposts=[i.serialize() for i in listposts])


if __name__ == '__main__':
    posts.run()
