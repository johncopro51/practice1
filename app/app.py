from flask import Flask, render_template, redirect, url_for, request, session, flash,jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import socket
from flask_redis import FlaskRedis


app= Flask(__name__)
redis_client = FlaskRedis(app)
app.secret_key='lol'

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///salaries.db"
app.config["SQALCHEMY_TRACK_MODIFICATIONS"]=False
db = SQLAlchemy(app)
class users(db.Model):
    _id= db.Column("id",db.Integer, primary_key=True)
    name=db.Column(db.String(100),nullable=False)

    def __init__(self,name):
        self.name=name


app.permanent_session_lifetime =  timedelta(days=2)
@app.route('/',methods= ['GET','POST'])
def home():
        if"username" in session:
            return redirect(url_for(''))
        if request.method=='POST':
            username=request.form['user']
            new_user=users(name=username)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('home'))
        return render_template('index.html',container=socket.gethostname())

@app.route('/names')
def names():
    json_array=[]
    for item in users.query.all():
            json_array.append({"name":str(item.name)})
            kaka=jsonify(json_array)
    return kaka



if __name__=='__main__':
    with app.app_context():
     db.create_all()

    app.run(debug=True,host = '0.0.0.0',port=3000,)