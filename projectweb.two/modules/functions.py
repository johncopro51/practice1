from modules.models import Comment,Post,Like,User,follow
from flask import session
from base64 import b64encode
import base64
from modules import db
from datetime import datetime,timedelta


'''Recursive function that would be used to gather all
nested comments for the original comment'''
def testing(checking,count=0,list=[]):
    """if the count is equal to zero the list will be emptied,
    with out this if statement the list will keep on adding items to 
    itself"""
    if count==0: 
        list.clear()
    count+=1
    test=Comment.query.filter_by(parent_id=checking.id).all()
    if test!=None:
        for item in test:
            count+=1
            list.append(item)
            a=Comment.query.filter_by(parent_id=item.id).all()
            if a:
                 testing(item,list=list,count=count)
            

    return  list
'''function to decode pictures saved in db'''
def render(data):
    render_pic = base64.b64encode(data).decode('ascii') 
    return render_pic
'''goes through every parent comment of the post and returns an organized list with all comments '''
def retrieve(list):
    children=[]
    for item in list:
        children.append(item)
        if testing(item)!=None:
            ag=testing(item)
            item.nested_comments=len(testing(item))
            db.session.commit()
            for item in ag:
                children.append(item)
        else:
            print('not working')  
    return children  

'''===================== quicksort to sort list ======================'''
def partition(array,low,high,key):
    pivot=array[high]
    i= low-1

    for j in range (low,high):
        if key(array[j])<= key(pivot):
            (array[i],array[j])=(array[j],array[i])

    (array[i+1],array[high]) = (array[high],array[i+1])

    return i + 1
def quickSort(array, low, high,key):
    if low<high:

        pivot= partition(array,low,high,key)

        quickSort(array,low,pivot - 1)

        quickSort(array,pivot + 1, high)

'''==================Liking Function=========================='''
def add_like(id):
    print('like')
    temp=Post.query.filter_by(id=id).first()
    if temp:

        temp.num_likes+=1
        db.session.commit()
    temp=Comment.query.filter_by(id=id).first()
    if temp:

        temp.num_likes+=1
        db.session.commit()

'''================== Remove Liking Function=========================='''
       
def remove_like(id):
    temp=Post.query.filter_by(id=id).first()
    print('unlike')

    if temp:
        temp.num_likes-=1
        db.session.commit()

    temp=Comment.query.filter_by(id=id).first()

    if temp:
        temp.num_likes-=1
        db.session.commit()
'''======================Liking System=============='''
def like(id,user):
            already_liked=Like.query.filter_by(LikeNOTE=id,user_id=user.id).first()
            if already_liked!=None:
                db.session.delete(already_liked)
                db.session.commit()
                remove_like(id)
            else:
                new_like=Like(LikeNOTE=id,username=session['username'],user_id=user.id)
                db.session.add(new_like)
                db.session.commit()
                add_like(id)


'''==================liking average=============='''
def top():
    Top=[]
    temporary_post= Post.query.all()
    length=len(temporary_post)
    total_likes=0
    for item in temporary_post:
        total_likes+=item.num_likes
    return(total_likes/length)
'''======================hot========================='''
def hot():
    hot=[]
    for item in Post.query.all():
        datetime_object =datetime.strptime(item.date,("%d") +" "+("%B")+"'"+("%y") + " "+ ("%I") +":"+ ("%M")+" "+ ("%p"))

        b=datetime.now()+timedelta(hours = 4)
        four_hours = str(b.strftime("%d")) +" "+ str(b.strftime("%B")) +"'"+ str(b.strftime("%y")) + " "+ str(b.strftime("%I")) +":"+ str(b.strftime("%M")) +" "+ str(b.strftime("%p"))
        average=top()
        if  item.date<four_hours and item.num_likes>average:
            hot.append(item)
            print(item)
            print(item.num_likes)
    hot.sort(key=lambda x: x.num_likes,reverse=True)
    return hot
'''========================================================sorting by days==========================================================='''
def sort(days,array):
        new_sorted=[]
        b=datetime.now()-timedelta(days = days)
        for item in array:
            item_date =datetime.strptime(item.date,("%d") +" "+("%B")+"'"+("%y") + " "+ ("%I") +":"+ ("%M")+" "+ ("%p"))
            if  item_date>=b:
                new_sorted.append(item)
                
        return new_sorted


''''===============================================getting all the authors for the array ==============================='''
def get_author(array):
    Author=[]
    if array:
        for item in array:
            temp=User.query.filter_by(username=item.username).first()
            Author.append(temp)
    return Author
'''============================================Getting the id's for all the liked item ======================================='''
def get_liked_ids(array):
    ids=[]
    if array:
        for item in array:
            ids.append(item.likeNOTE)
    return ids
'''=============================================== REPLYING================================================='''
def new_reply(reply,oc_id):
    main=Comment.query.filter_by(id=oc_id).first()
    x = datetime.now()
    currentTime = str(x.strftime("%d")) +" "+ str(x.strftime("%B")) +"'"+ str(x.strftime("%y")) + " "+ str(x.strftime("%I")) +":"+ str(x.strftime("%M")) +" "+ str(x.strftime("%p"))
    new_comment=Comment(comment=reply,post_id=main.post_id,parent_id=main.id,level=main.level+1,username=session['username'],date=currentTime)
    db.session.add(new_comment)
    main.has_children=True
    db.session.commit()
    '''================================================commenting======================================'''
def new_comment(comment,post_id):
    x = datetime.now()
    currentTime = str(x.strftime("%d")) +" "+ str(x.strftime("%B")) +"'"+ str(x.strftime("%y")) + " "+ str(x.strftime("%I")) +":"+ str(x.strftime("%M")) +" "+ str(x.strftime("%p"))
    new_comment=Comment(comment=comment,username=session['username'],post_id=post_id,date=currentTime)
    db.session.add(new_comment)
    db.session.commit()
    '''======================================================getting post of followed people=================================='''
def get_followed_post():
    followed_post_list=[]
    following_post=follow.query.filter_by(username=session['username']).all()
    if following_post:
        for item in following_post:
            temp= Post.query.filter_by(username=item.username2).all()
            if temp:
                for item in temp:
                    followed_post_list.append(item)
    return followed_post_list



         



