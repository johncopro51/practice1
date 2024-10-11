from flask import Flask,render_template, redirect, url_for, flash, request,session,jsonify
from modules import app,db,bcrypt
from modules.models import User, Post, Comment,Like,follow,Chat
from modules.functions import render,testing,retrieve,remove_like,add_like,like,top,hot,sort,get_author,new_reply,new_comment,get_followed_post
from datetime import timedelta, datetime
import re


@app.route('/')
def index():

    return redirect(url_for('dash'))

'''=========================================================='''
'''======================== account creation ================'''
'''=========================================================='''
#note: this could easily be done using Flask_login library
@app.route('/sign-up',methods=['GET','POST'])
def sign_up():
    if"username" in session:
        return redirect(url_for('dash'))
    else:

        if request.method=='POST':
            username=request.form['username']
            password=request.form['password']
            password2=request.form['password2']
            #checking if the username exist in db
            found_user = User.query.filter_by(username=username).first()    
            if found_user:

                flash('user exist', category='error')
            #checking if passwords match
            elif password2!=password:

                flash('paswords need to match', category='error')
            else:

                #if all conditionals are met and no errors occur a new account will be made
                hashed_password = bcrypt.generate_password_hash(password)
                

                f = open('modules/image.txt', 'r')
                render_file = f.read()
                new_user=User(username=username,password=hashed_password,rendered_data=render_file)
                #create a new session 
                session['username'] = username
                db.session.add(new_user)
                db.session.commit()

                return redirect(url_for('dash'))
            
    return render_template('sign_up.html')

'''============================================================================'''
''''================================= Account Login =========================='''
'''============================================================================'''
@app.route('/login',methods=['GET','POST'])
def login():
    if"username" in session:
        return redirect(url_for('dash'))
    else:

        if request.method=='POST':
            username=request.form['username']
            password=request.form['password']
            found_user = User.query.filter_by(username=username).first() 
            if found_user:

                if bcrypt.check_password_hash(found_user.password,password):
                    session['username'] = username
                    return redirect(url_for('dash'))
                else:
                    flash("wrong password", category='error')
            else:
                flash("no user found", category='error')

    return render_template('login.html')
'''==========================================================================================='''
''''===========================  POSTING ACTION =============================================='''
'''==========================================================================================='''

@app.route('/post',methods=['GET','POST'])
def post():

    if"username" not in session:
        return redirect(url_for('dash'))
    else:
        if request.method=='POST':

            username=session['username']
            note=request.form['note']
            title=request.form['title']
            file = request.files['inputFile']
            test=str(file)
            a=test.replace('/', ' ')
            a=a.replace("'", ' ')
            print(a)
            if 'image'in a:
                type='image'
            elif 'video'in a:
                type='video'
            else:
                type='none'
            data = file.read()
            render_file = render(data)
            #if no file has been uploaded it will be set to zero
            if len(render_file)==0:
                render_file=0
            x = datetime.now()
            currentTime = str(x.strftime("%d")) +" "+ str(x.strftime("%B")) +"'"+ str(x.strftime("%y")) + " "+ str(x.strftime("%I")) +":"+ str(x.strftime("%M")) +" "+ str(x.strftime("%p"))
            new_Note=Post(note=note,title=title,username=username,date=currentTime,name=file.filename, data=data, rendered_data=render_file,type=type)
            db.session.add(new_Note)
            db.session.commit()
            return redirect(url_for('dash'))



    return render_template('posting.html')
'''===================================================================='''
'''=======================    Dashboard     ========================'''
'''===================================================================='''

@app.route("/dash",methods=['GET','POST'])
def dash():
    if"username" not in session:
        return redirect(url_for('guest_dash'))
    else:
        post=Post.query.all()
        User_liked_id=[]
        current_user=User.query.filter_by(username=session['username']).first()
        Author=get_author(post)



        Current_like=Like.query.filter_by(username=session['username']).all()
        liked_post=[]
        for item in Current_like:
            User_liked_id.append(item.LikeNOTE)

            if Post.query.filter_by(id=item.LikeNOTE).first():
                        liked_post.append(Post.query.filter_by(id=item.LikeNOTE).first())
                        
        if 'like' in request.form:

            id=request.form['like']
            Current_session=User.query.filter_by(username=session['username']).first()
            like(id,Current_session)

        if 'search' in request.form:

            search=request.form['search']
            if len(search)!=0:
                return  redirect('/search/'+search)
        if 'follow' in request.form:
            post=get_followed_post()
            Author=get_author(post)
            return render_template('user_dash.html',Author=Author,post=post,current_user=current_user,User_liked_id=User_liked_id,field='follow')


        if 'new' in request.form:
            post=Post.query.order_by(Post.date).all()
            post.reverse()
            Author=get_author(post)
            return render_template('user_dash.html',Author=Author,post=post,current_user=current_user,User_liked_id=User_liked_id,field='new')

        if 'top' in request.form:

            post=Post.query.order_by(Post.num_likes).all()
            post.reverse()
            Author=get_author(post)

            return render_template('user_dash.html',Author=Author,post=post,current_user=current_user,User_liked_id=User_liked_id,field='top')
        
        if 'liked' in request.form:

            Author=get_author(liked_post)    

            return render_template('user_dash.html',Author=Author,post=liked_post,current_user=current_user,User_liked_id=User_liked_id,field='liked')
        if 'active' in request.form:
                
                post=hot()
                Author=get_author(post)
                
                return render_template('user_dash.html',Author=Author,post=post,current_user=current_user,User_liked_id=User_liked_id,field='active')
        if 'mypost' in request.form:

            post=Post.query.filter_by(username=session['username']).all()
            Author=get_author(post)

            return render_template('user_dash.html',Author=Author,post=post,current_user=current_user,User_liked_id=User_liked_id,field='mypost')
        
        if 'days' in request.form:

            days= request.form['days']
            da=int(''.join(x for x in days if x.isdigit()))
            letters=" ".join(re.findall("[a-zA-Z]+", days))
            '''sorting the following by days'''
            if letters=='follow':
                post=get_followed_post()
                post=sort(da,post)
                Author=get_author(post)
                return render_template('user_dash.html',Author=Author,post=post,current_user=current_user,User_liked_id=User_liked_id,field='follow')

            if letters=='new':
                post=Post.query.order_by(Post.date).all()
                post.reverse()
                post=sort(da,post)
                print(sort(da, post))
                Author=get_author(post)
                return render_template('user_dash.html',Author=Author,post=post,current_user=current_user,User_liked_id=User_liked_id,field='new')

            if letters=='top':
                post=Post.query.order_by(Post.num_likes).all()
                post.reverse()
                post=sort(da,post)
                Author=get_author(post)

                return render_template('user_dash.html',Author=Author,post=post,current_user=current_user,User_liked_id=User_liked_id,field='top')
            if letters=='regular':
                post=sort(da,post)
                Author=get_author(post)

                return render_template('user_dash.html',Author=Author,post=post,current_user=current_user,User_liked_id=User_liked_id,field='regular')

            
            if letters=='liked':
                post=sort(da,liked_post)
                Author=get_author(post)

                return render_template('user_dash.html',Author=Author,post=post,current_user=current_user,User_liked_id=User_liked_id,field='liked')



        return render_template('user_dash.html',Author=Author,post=post,current_user=current_user,User_liked_id=User_liked_id,field='regular')



'''====================================   MAIN POST VIEWING  =============================================================='''


@app.route("/comment/<int:post_id>",methods=['GET','POST'])
def comment(post_id):
    if"username" not in session:
        return redirect(url_for('guest_dash'))
    else:
        '''getting user information as well as post to display in dash.'''
        user=User.query.filter_by(username=session['username']).first()
        post=Post.query.filter_by(id=post_id).first()
        Author=User.query.filter_by(username=post.username).first()
        Parents=Comment.query.filter_by(post_id=post_id,parent_id=None).all()
        Full_Comments=retrieve(Parents)
        Comment_Author=get_author(Full_Comments)
        User_liked_id=[]
        Current_like=Like.query.filter_by(username=session['username']).all()
        for item in Current_like:
            User_liked_id.append(item.LikeNOTE)
        if request.method=='POST':
            if 'search' in request.form:
                search=request.form['search']
                if len(search)!=0:
                    return  redirect('/search/'+search)
                
            if 'c' in request.form:
                comment=request.form['c']
                if len(comment)!=0:
                    new_comment(comment,post_id)

            if 'reply' in request.form:
                    reply=request.form['reply']
                    orig_comment_id=request.form['og']
                    if len(reply)!=0:
                        new_reply(reply,orig_comment_id)

            if 'like' in request.form:

                id=request.form['like']
                Current_session=User.query.filter_by(username=session['username']).first()
                like(id,Current_session)

            if 'top' in request.form:

                Parents=Comment.query.filter_by(post_id=post_id,parent_id=None).order_by(Comment.num_likes).all()
                Parents.reverse()
                Full_Comments=retrieve(Parents)
                Comment_Author=get_author(Full_Comments)

                return render_template('main_post.html',user=user,Comment_Author=Comment_Author,Author=Author,post=post,comments=Full_Comments,User_liked_id=User_liked_id)
            

            if 'new' in request.form:
                Parents=Comment.query.filter_by(post_id=post_id,parent_id=None).order_by(Comment.date).all()
                Parents.reverse()
                Full_Comments=retrieve(Parents)
                Comment_Author=get_author(Full_Comments)

                return render_template('main_post.html',user=user,Comment_Author=Comment_Author,Author=Author,post=post,comments=Full_Comments,User_liked_id=User_liked_id)
            
            
            if 'active' in request.form:
                Parents=Comment.query.filter_by(post_id=post_id,parent_id=None).order_by(Comment.nested_comments).all()
                Parents.reverse()
                Full_Comments=retrieve(Parents)
                Comment_Author=get_author(Full_Comments)

                return render_template('main_post.html',user=user,Comment_Author=Comment_Author,Author=Author,post=post,comments=Full_Comments,User_liked_id=User_liked_id)
            
        return render_template('main_post.html',user=user,Comment_Author=Comment_Author,Author=Author,post=post,comments=Full_Comments,User_liked_id=User_liked_id)




'''====================================SEARCHING=============================================='''
@app.route('/search/<string:search_get>',methods=['GET','POST'])
def search(search_get):
    if"username" not in session:
        return redirect(url_for('guest_dash'))
    else:
        current_user=User.query.filter_by(username=session['username']).first()
        result=[]
        post=Post.query.all()
        for item in post:
            if search_get in item.note or search_get in item.title:
                result.append(item)

        Author=get_author(result)



        if 'search' in request.form:
                search=request.form['search']
                if len(search)!=0:
                    return  redirect('/search/'+search)
                
            
        if 'like' in request.form:
            id=request.form['like']
            Current_session=User.query.filter_by(username=session['username']).first()
            like(id,Current_session)
        
        if 'comment' in request.form:
            result_comment=[]
            comment=Comment.query.all()
            for item in comment:
                if search_get in item.comment:
                    result_comment.append(item)
            Author=get_author(result_comment)
            if  len(result_comment)==0:
                '''if no comment found flash the following message'''

                flash("No Comments found", category='error')

            return render_template('search.html',Author=Author,current_user=current_user,post=[],result_comment=result_comment)
        
        if 'users' in request.form:
            result_user=[]
            users=User.query.all()
            for item in users:
                if search_get in item.username:
                    result_user.append(item) 
            if  len(result_user)==0:
                '''if no users found flash the following message'''
                flash("No users found", category='error')
        
            return render_template('search.html',current_user=current_user,post=[],result_comment=[],result_user=result_user)
        if len(result)==0:
            '''if no post found flash the following message'''
            flash("No Post Found", category='error')


        return render_template('search.html',Author=Author,current_user=current_user,post=result)

'''================================PROFILE================================================='''


@app.route('/profile/<string:PF_PAGE>',methods=['GET','POST'])
def profile(PF_PAGE):
    if"username" not in session:
        return redirect(url_for('guest_dash'))
    else:
        profile=User.query.filter_by(username=PF_PAGE).first()
        current_user=User.query.filter_by(username=session['username']).first()
        '''getting top post of user if there is one'''
        Top_post=Post.query.filter_by(username=PF_PAGE).order_by(Post.num_likes).all()
        Top_post.reverse()
        if len(Top_post)!=0:

            Top_post=(Top_post[0])
        '''getting top comment of user if there is one'''

        Top_comment=Comment.query.filter_by(username=PF_PAGE).order_by(Comment.num_likes).all()
        Top_comment.reverse()
        if len(Top_comment)!=0:

            Top_comment=(Top_comment[0])

        post=Post.query.filter_by(username=PF_PAGE).all()
        comments=Comment.query.filter_by(username=PF_PAGE).all()
        Likes_list=[]
        likes=Like.query.filter_by(username=PF_PAGE).all()
        '''getting all the liked post/comments for the profile being viewed'''
        for item in likes:
            if Post.query.filter_by(id=item.LikeNOTE).first():

                Likes_list.append(Post.query.filter_by(id=item.LikeNOTE).first())
            if Comment.query.filter_by(id=item.LikeNOTE).first():

                Likes_list.append(Comment.query.filter_by(id=item.LikeNOTE).first())

        Authors=get_author(Likes_list)

        '''getting to see if the the user is following or not'''   
        following_field=follow.query.filter_by(username=session['username'],username2=PF_PAGE).first()

        if following_field!=None:

            following_field='following'
        else:

            following_field='not_following'
        if 'chat' in request.form:
            first_user=User.query.filter_by(username=session['username']).first()
            second_user=User.query.filter_by(username=PF_PAGE).first()

            if Chat.query.filter_by(username=first_user.username,username2=second_user.username).first():
                rn=Chat.query.filter_by(username=first_user.username,username2=second_user.username).first()
                return  redirect('/room/'+str(rn.id))

            elif Chat.query.filter_by(username=second_user.username,username2=first_user.username).first():
                rn=Chat.query.filter_by(username=first_user.username,username2=second_user.username).first()
                return  redirect('/room/'+str(rn.id))
                '''checking to see if chat room exist if not we will create one'''
            else:

                New_room=Chat(username=first_user.username,username2=second_user.username)
                db.session.add(New_room)
                db.session.commit()
                return  redirect('/room/'+str(New_room.id))
            


        if "FOLLOW" in request.form:
            alreadyfollows=follow.query.filter_by(username=session['username'],username2=PF_PAGE).first()
            if alreadyfollows:

                if (alreadyfollows.username==session['username']):

                    print ('unfollow')
                    db.session.delete(alreadyfollows)
                    db.session.commit()

            else:

                new_follow=follow(username=session['username'],username2=PF_PAGE)
                print('following')
                db.session.add(new_follow)
                db.session.commit()

        if 'search' in request.form:
                search=request.form['search']
                if len(search)!=0:
                    return  redirect('/search/'+search)
        if "likes" in request.form:
            return render_template('profile.html',Top_post=Top_post,Top_comment=Top_comment,Likes_list=Likes_list,profile=profile,current_user=current_user,Authors=Authors)
        
        if 'comment' in request.form:
            return render_template('profile.html',Top_post=Top_post,Top_comment=Top_comment,comments=comments,profile=profile,current_user=current_user,)
        
        if 'post' in request.form:
            return render_template('profile.html',Top_post=Top_post,Top_comment=Top_comment,post=post,profile=profile,current_user=current_user)
        
        return render_template('profile.html',Top_post=Top_post,Top_comment=Top_comment,post=post,profile=profile,current_user=current_user,following_field=following_field)

'''================================ EDIT PROFILE================================================='''

@app.route('/profile/edit/<string:PF_PAGE>',methods=['GET','POST'])
def edit_profile(PF_PAGE):
    if"username" not in session:
        return redirect(url_for('guest_dash'))
    else:
        current_user=User.query.filter_by(username=session['username']).first() 

        if request.method=='POST':

            bio=request.form['bio']
            file = request.files['inputFile']
            test=str(file)
            a=test.replace('/', ' ')
            a=a.replace("'", ' ')
            '''we will only accepts image formats'''
            if 'image'in a:

                data = file.read()
                
                render_file = render(data)
                print(render_file)
                current_user.name=file.filename
                current_user.data=data
                current_user.rendered_data=render_file
            '''if nothing was typed in the bio section we will leave it unchanged'''
            if len(bio)>0:
                current_user.bio=bio

            db.session.commit()
            return redirect('/profile/'+PF_PAGE)

        

        return render_template('edit_profile.html',current_user=current_user)

'''================================ Logout  ========================'''
@app.route('/logout')
def logout():
   session.pop('username', None)
   return redirect(url_for('dash'))
