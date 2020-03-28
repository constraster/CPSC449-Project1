from datetime import datetime
import os
import pytz
from pytz import timezone
import request
from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime

users = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
users.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'logs.db')
db = SQLAlchemy(users)
mar = Marshmallow(users)

def get_time():
    date = datetime.now(tz=pytz.utc)
    date = date.astimezone(timezone('US/Pacific'))
    pstTime = date
    return pstTime


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    karma = Column(Integer, default=0)
    createtime = Column(DateTime, default=get_time())
    changetime = Column(DateTime, default=get_time())

class UserData(mar.Schema):
    class Data:
        fields = ('id', 'username', 'email', 'password', 'karma', 'createtime', 'changetime')


userdata = UserData()
usermultdata = UserData(many=True)


@users.cli.command('create_db')
def create_db():
    db.create_all()
    print('created a database')


@users.cli.command('drop_db')
def drop_db():
    db.drop_all()
    print('dropped the db')


@users.cli.command('seed_db')
def seed_db():

    test = User(username='FrancisNguyen', email="test@gmail.com", password='testpass', karma=12)

    db.session.add(test)
    db.session.commit()
    print('DB seeded')


@users.route('/')
def index():
    return 'Hello World'


# Register users
@users.route('/v1/api/user/register', methods=['POST'])
def register():
    email = request.form['email']
    username = request.form['username']
    regis = User.query.filter_by(email=email).first() and User.query.filter_by(username=username).first()
    if regis:
        return jsonify(message='Email or Username Already exists'), 409
    else:
        username = request.form['username']
        password = request.form['password']
        karma = request.form['karma']
        createtime = get_time()
        changetime = get_time()
        user = User(username=username, email=email, password=password,
                    karma=karma, createtime=createtime, changetime=changetime)
        db.session.add(user)

        db.session.commit()
        return jsonify(message='User created'), 201


# increment karma
@users.route('/v1/api/user/add_karma', methods=['PUT'])
def add_karma():
    username = request.form['username']
    user = User.query.filter_by(username=username).first()
    if user:
        user.karma += 1
        db.session.commit()
        return jsonify(message='Added karma'), 202
    else:
        return jsonify('Could not add karma'), 404


# decrement karma
@users.route('/v1/api/user/sub_karma', methods=['PUT'])
def sub_karma():
    username = request.form['username']
    user = User.query.filter_by(username=username).first()
    if user:
        user.karma -= 1
        db.session.commit()
        return jsonify(message='Subtracted karma!'), 202
    else:
        return jsonify('Could not subtract karma'), 404


# update user's email
@users.route('/v1/api/user/update_email', methods=['PUT'])
def update_email():
    username = request.form['username']
    usersemail = User.query.filter_by(username=username).first()
    if usersemail:
        usersemail.email = request.form['email']
        usersemail.createtime = get_time()
        db.session.commit()
        return jsonify(message='Email updated'), 202
    else:
        return jsonify('This user does not exist'), 404


# delete user's account
@users.route('/v1/api/user/deactivate_acc/<string:username>', methods=['DELETE'])
def deactivate_account(username: str):
    username = User.query.filter_by(username=username).first()
    if username:
        db.session.delete(username)
        db.session.commit()
        return jsonify(message="deleted a user"), 202
    else:
        return jsonify(message="User doesn't exist"), 404


if __name__ == '__main__':
    users.run()
