from app import db
from hashlib import md5
from sqlalchemy import or_,and_

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    username = db.Column(db.String(80),unique=True)
    password = db.Column(db.String(80))

    def avatar(self,size):
        return 'http://www.gravatar.com/avatar/' + md5(self.email.encode('utf-8')).hexdigest() + '?d=mm&s=' + str(size)

    #判断账号是否存在
    def Account_Judgment(self,username,password):
        user = User.query.filter(and_(User.username == username,User.password == password)).first()
        if user == None:
            return False
        else:
            return True

    #判断邮箱、用户名是否注册过
    def valid_regist(self,username_value,email_value):
        user = User.query.filter(or_(User.username == username_value,User.email == email_value)).first()
        if user == None:
            return True
        else:
            return False

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % (self.username)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)
