from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
app= Flask(__name__)
app.secret_key='lol'

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///salaries.db"
app.config["SQALCHEMY_TRACK_MODIFICATIONS"]=False
db = SQLAlchemy(app)
class users(db.Model):
    _id= db.Column("id",db.Integer, primary_key=True)
    name=db.Column(db.String(100),nullable=False)

    def __init__(self,name,email):
        self.name=name
        self.email=email


app.permanent_session_lifetime =  timedelta(days=2)
@app.route('/')
def home():
    return render_template('index.html')



if __name__=='__main__':
    with app.app_context():
     db.create_all()

    app.run(debug=True)