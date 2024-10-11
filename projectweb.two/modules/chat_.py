from flask import Flask,render_template, redirect, url_for, flash, request,session,jsonify
from modules import app,db,bcrypt,socketio
from modules.models import User,Comment,Message,Chat
from modules.functions import get_author
from datetime import datetime

import re
from flask_socketio import send,emit,join_room


@app.route('/room/<int:rn>',methods=['GET','POST'])
def newroom(rn):
    chat=Chat.query.filter_by(id=rn).first()
    if"username" not in session:
        return redirect(url_for('dash'))

    elif session["username"] == chat.username or session["username"] == chat.username2:
        '''getting chat messages and authors for the messages'''
        current_user=User.query.filter_by(username=session['username']).first()
        Messages=Message.query.filter_by(Chat_id=rn).all()
        Authors=get_author(Messages)
        if 'search' in request.form:
            search=request.form['search']
            if len(search)!=0:
                return  redirect('/search/'+search)

        return render_template('chat.html',rn=rn,Messages=Messages,Authors=Authors,current_user=current_user)
    else:
        return redirect(url_for('dash'))
    
@app.route('/chat_dash',methods=['GET','POST'])
def chat_dash():
    if"username" not in session:
        return redirect(url_for('dash'))
    else:  
        '''getting all the chats that the user is a part of'''
        current_user=User.query.filter_by(username=session['username']).first()
        chats=Chat.query.filter_by(username2=session['username']).all()
        chat_author=[]
        chat_author=get_author(chats)
        '''using for loop to get all the opposite users of that chatroom to display'''
        for item in Chat.query.filter_by(username=session['username']).all():
            chats.append(item)
            temp=User.query.filter_by(username=item.username2).first()
            chat_author.append(temp)
        if 'search' in request.form:
            search=request.form['search']
            if len(search)!=0:
                return  redirect('/search/'+search)

    return render_template('chat_dash.html',chats=chats,chat_author=chat_author,current_user=current_user)

     




@socketio.on('send_message')
def send_message(message):
    print('message: '+message['data'])
    a=message['data']
    rn=message['room']
    x = datetime.now()
    currentTime = str(x.strftime("%d")) +" "+ str(x.strftime("%B")) +"'"+ str(x.strftime("%y")) 
    new_message=Message(message=a,Chat_id=rn,username=session['username'],date=currentTime)
    '''retrieving message, saving it to the database, and then emmiting it in the specific chatroom for other users to see.'''
    db.session.add(new_message)
    db.session.commit()
    current_user=User.query.filter_by(username=session['username']).first()
    emit('my_response',{'message': a,'username':current_user.username,'pf_pic':current_user.rendered_data},room=str(rn),broadcast=True)
    

@socketio.on('join')
def join(data):
	join_room(data['room'])
