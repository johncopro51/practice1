from flask import Flask,render_template, redirect, url_for, flash, request,session,jsonify
from modules import app,db,bcrypt
from modules.models import User, Post, Comment,Like,follow
from modules.functions import render,testing,retrieve,remove_like,add_like,like,top,hot,sort,get_author,new_reply,new_comment
from datetime import timedelta, datetime
import re
'''++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'''
'''++++++++++++++++++++++++++++++++++++++++                     GUEST DASH               ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'''
'''++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'''

@app.route("/guest",methods=['GET','POST'])
def guest_dash():
    if"username"  in session:
        return redirect(url_for('dash'))
    else:
        post=Post.query.all()
        Author=get_author(post)
        if 'search' in request.form:

            search=request.form['search']
            if len(search)!=0:
                    return  redirect('/guest/search/'+search)
            
        if 'new' in request.form:
            post=Post.query.order_by(Post.date).all()
            post.reverse()
            Author=get_author(post)
            return render_template('guest_dash.html',Author=Author,post=post,field='new')
        
        if 'top' in request.form:

            post=Post.query.order_by(Post.num_likes).all()
            post.reverse()
            Author=get_author(post)

            return render_template('guest_dash.html',Author=Author,post=post,field='top')
        
        if 'active' in request.form:
                
                post=hot()
                Author=get_author(post)
                
                return render_template('guest_dash.html',Author=Author,post=post,field='active')

        if 'days' in request.form:

            days= request.form['days']
            da=int(''.join(x for x in days if x.isdigit()))
            letters=" ".join(re.findall("[a-zA-Z]+", days))

            if letters=='top':
                post=Post.query.order_by(Post.num_likes).all()
                post.reverse()
                post=sort(da,post)
                Author=get_author(post)

                return render_template('testing.html',Author=Author,post=post,field='top')
            if letters=='new':
                post=Post.query.order_by(Post.date).all()
                post.reverse()
                post=sort(da,post)
                Author=get_author(post)
                return render_template('guest_dash.html',Author=Author,post=post,field='new')


        return render_template('guest_dash.html',Author=Author,post=post,field='regular')


'''++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'''
'''+++++++++++++++++++++++++++++++++++++++ GUEST POST VIEWING ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'''
'''++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'''

@app.route("/guest/comment/<int:post_id>",methods=['GET','POST'])
def guest_comment(post_id):
    if"username"  in session:
        return redirect(url_for('dash'))
    else:
        post=Post.query.filter_by(id=post_id).first()
        Author=User.query.filter_by(username=post.username).first()
        Parents=Comment.query.filter_by(post_id=post_id,parent_id=None).all()
        Full_Comments=retrieve(Parents)
        Comment_Author=get_author(Full_Comments)


        if request.method=='POST':
            if 'search' in request.form:
                search=request.form['search']
                if len(search)!=0:
                    return  redirect('/guest/search/'+search)
            if 'top' in request.form:

                Parents=Comment.query.filter_by(post_id=post_id,parent_id=None).order_by(Comment.num_likes).all()
                Parents.reverse()
                Full_Comments=retrieve(Parents)
                Comment_Author=get_author(Full_Comments)

                return render_template('guest_post_viewing.html',Comment_Author=Comment_Author,Author=Author,post=post,comments=Full_Comments)
            

            if 'new' in request.form:
                Parents=Comment.query.filter_by(post_id=post_id,parent_id=None).order_by(Comment.date).all()
                Parents.reverse()
                Full_Comments=retrieve(Parents)
                Comment_Author=get_author(Full_Comments)

                return render_template('guest_post_viewing.html',Comment_Author=Comment_Author,Author=Author,post=post,comments=Full_Comments)
            
            
            if 'active' in request.form:
                Parents=Comment.query.filter_by(post_id=post_id,parent_id=None).order_by(Comment.nested_comments).all()
                Parents.reverse()
                Full_Comments=retrieve(Parents)
                Comment_Author=get_author(Full_Comments)

                return render_template('guest_post_viewing.html',Comment_Author=Comment_Author,Author=Author,post=post,comments=Full_Comments)
            
        return render_template('guest_post_viewing.html',Comment_Author=Comment_Author,Author=Author,post=post,comments=Full_Comments)


'''++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'''
'''+++++++++++++++++++++++++++++++++++++++ GUEST profile Viewing ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'''
'''+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'''

@app.route('/guest/profile/<string:PF_PAGE>',methods=['GET','POST'])
def guest_profile_view(PF_PAGE):
    if"username"  in session:
        return redirect(url_for('dash'))
    else:
        profile=User.query.filter_by(username=PF_PAGE).first()
        Top_post=Post.query.filter_by(username=PF_PAGE).order_by(Post.num_likes).all()
        Top_post.reverse()
        if len(Top_post)!=0:
            Top_post=(Top_post[0])

        Top_comment=Comment.query.filter_by(username=PF_PAGE).order_by(Comment.num_likes).all()
        Top_comment.reverse()
        if len(Top_comment)!=0:
            Top_comment=(Top_comment[0])

        post=Post.query.filter_by(username=PF_PAGE).all()
        comments=Comment.query.filter_by(username=PF_PAGE).all()
        Likes_list=[]
        likes=Like.query.filter_by(username=PF_PAGE).all()
        for item in likes:
            if Post.query.filter_by(id=item.LikeNOTE).first():
                Likes_list.append(Post.query.filter_by(id=item.LikeNOTE).first())
            if Comment.query.filter_by(id=item.LikeNOTE).first():
                Likes_list.append(Comment.query.filter_by(id=item.LikeNOTE).first())
            
        Authors=get_author(Likes_list)

        if 'search' in request.form:
                search=request.form['search']
                if len(search)!=0:
                    return  redirect('/guest/search/'+search)

        if "likes" in request.form:
            return render_template('guest_profile_viewing.html',Top_post=Top_post,Top_comment=Top_comment,Likes_list=Likes_list,profile=profile,Authors=Authors)
        if 'comment' in request.form:
            return render_template('guest_profile_viewing.html',Top_post=Top_post,Top_comment=Top_comment,comments=comments,profile=profile,)
        if 'post' in request.form:
            return render_template('guest_profile_viewing.html',Top_post=Top_post,Top_comment=Top_comment,post=post,profile=profile)
        

        return render_template('guest_profile_viewing.html',Top_post=Top_post,Top_comment=Top_comment,post=post,profile=profile,)

'''++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'''
'''+++++++++++++++++++++++++++++++++++++++ GUEST Search ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'''
'''+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'''
@app.route('/guest/search/<string:search_get>',methods=['GET','POST'])
def guest_search(search_get):
    if"username"  in session:
        return redirect(url_for('dash'))
    else:
        result=[]
        post=Post.query.all()
        for item in post:
            if search_get in item.note or search_get in item.title:
                result.append(item)

        Author=get_author(result)

        if 'search' in request.form:
                search=request.form['search']
                if len(search)!=0:
                    return  redirect('/guest/search/'+search)
        
        if 'comment' in request.form:
            result_comment=[]
            comment=Comment.query.all()
            for item in comment:
                if search_get in item.comment:
                    result_comment.append(item)
            Author=get_author(result_comment)
            if  len(result_comment)==0:
                flash("No Comments found", category='error')

            return render_template('guest_search.html',Author=Author,post=[],result_comment=result_comment)
        if 'users' in request.form:
            result_user=[]
            users=User.query.all()
            for item in users:
                if search_get in item.username:
                    print('found one')
                    result_user.append(item) 
            if  len(result_user)==0:
                flash("No users found", category='error')
        
            return render_template('guest_search.html',post=[],result_comment=[],result_user=result_user)
        if len(result)==0:
            flash("No Post Found", category='error')


        return render_template('guest_search.html',Author=Author,post=result)