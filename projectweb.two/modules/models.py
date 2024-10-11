from modules import db
'''I got rid of all string caps due to postgre having issues and just decided to put out errors if user  to exceeds string size'''
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String,nullable=False,unique=True)
    password= db.Column(db.LargeBinary,nullable=False,)
    posts = db.relationship('Post',backref='user')
    likes = db.relationship('Like',backref='user')

        # required data field to save file to db
    data = db.Column(db.LargeBinary) 
    rendered_data = db.Column(db.Text)
    name = db.Column(db.String(128))
    bio=db.Column(db.String)


class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    note= db.Column(db.String)
    title= db.Column(db.String,nullable=False)
    num_likes=db.Column(db.Integer,default=0)
    username=db.Column(db.String,nullable=False)
    type=db.Column(db.String)
    date = db.Column(db.String)
    # required data field to save file to db
    data = db.Column(db.LargeBinary) 
    rendered_data = db.Column(db.Text)
    name = db.Column(db.String)
    # save file end
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref='post')

class Comment(db.Model):


    id = db.Column(db.Integer, primary_key=True)
    comment= db.Column(db.String,nullable=False)
    num_likes=db.Column(db.Integer,default=0)
    username=db.Column(db.String,nullable=False)
    date = db.Column(db.String)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    nested_comments=db.Column(db.Integer,default=0)
    has_children=db.Column(db.Boolean,default=False )
    #level that would be used to display the depth of the threaded comment
    level=db.Column(db.Integer,default=0) 
    # we could gather all children for the comment via query by parent_id
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]),
        lazy='dynamic')

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    LikeNOTE= db.Column(db.Integer)
    username=db.Column(db.String,nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
class follow(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String,nullable=False)
    username2= db.Column(db.String,nullable=False)

class Chat(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String,nullable=False)
    username2= db.Column(db.String,nullable=False)

class Message(db.Model):


    id = db.Column(db.Integer, primary_key=True)
    message= db.Column(db.String,nullable=False)
    username= db.Column(db.String,nullable=False)
    Chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'))
    date = db.Column(db.String)



