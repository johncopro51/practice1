from flask import Flask, render_template, redirect, url_for, request, session, flash,jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import socket

app= Flask(__name__)
app.secret_key='lol'

app.config['SQLALCHEMY_DATABASE_URI']= "postgresql://root:root@postgresql-master:5432/test_db1"
db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String,nullable=False,unique=False)



app.permanent_session_lifetime =  timedelta(days=2)

@app.route('/',methods= ['GET','POST'])
def home():
        if"username" in session:
            return redirect(url_for(''))
        if request.method=='POST':
            username=request.form['user']
            new_user=User(username=username)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('home'))
        return render_template('index.html',container=socket.gethostname())

@app.route('/names')
def names():
    json_array=[]
    for item in User.query.all():
            json_array.append({"name":str(item.username)})
            kaka=jsonify(json_array)
    return kaka



if __name__=='__main__':
    with app.app_context():
     db.create_all()

    app.run(debug=True,host = '0.0.0.0',port=3000,)