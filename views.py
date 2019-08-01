import os
import secrets
from app import app, db, bcrypt, login_manager
import service.user,service.post,service.relation,service.general
import json
import test
from flask import render_template,request,url_for, flash, redirect,session
from forms import PostForm, RegistrationForm,LoginForm,UploadUserImageForm, UpdateAccountForm, RelationForm
from models import User, Post
from flask_login import login_user, current_user, logout_user,login_required
from PIL import Image

@app.route("/",methods=['GET', 'POST']) 
@app.route("/index",methods=['GET', 'POST'])
@login_required
def main():

    if current_user.is_authenticated:
        postform = PostForm()
        if postform.validate_on_submit():
            if postform.postimage:
                file = postform.postimage.data 
                url = service.general.UploadImage(file)
                newpost = service.post.AddPost(postform.text.data,current_user.id,url)
            
            else:
                newpost = service.post.AddPost(postform.text.data,current_user.id)
 
        return render_template('index.html', title='home',current_user=current_user,newposts = GetRecentPosts(),postform = postform)

    else:
        return redirect(url_for('login'))
    
@app.route("/search",methods=['POST'])
def search():   
    users = []
    content = request.get_json()
    result = service.user.Search(content['text'])
    for user in result:
        username_userid = str(user.id)+"-"+user.name
        users.append(username_userid)
    users_obj = {}
    users_obj["searchresult"] = users
    json_data = json.dumps(users_obj)
    return json_data

@app.route("/user/add/<name>/<email>")
def add_user(name,email):
    result = service.user.AddUser(name,email)
    if result:
        return "Successfully added!"


@app.route("/user/<id>")
def get_user(id):
    result = service.user.GetUserById(int(id))
    return result


@app.route("/post/add/<text>")
def add_post(text):
    result = service.post.AddPost(text,current_user.id)
    return result


@app.route("/post/<id>")
def get_post(id):
    result = service.post.GetPostById(int(id))
    return result.text

@app.route("/post/upload/",methods=['GET', 'POST'])
def upload_image():
    form = PostForm()
    if form.validate_on_submit():
        file = request.files['file']
        service.general.UploadImage(file)
    return render_template('upload.html', title='Upload image', form=form)

@app.route("/user/upload/",methods=['POST'])
def upload_user_image(id=None):

    result =""
    form = UploadUserImageForm()
    if form.validate_on_submit():
        img_url = service.general.UploadImage(form.userimage.data)
        if img_url:
            #update user
            service.user.UpdateProfileImage(current_user.id,img_url)
            return profile(current_user.id,img_url)
        else:
            # should modifty this case!!!
            return redirect(url_for('profile',id=current_user.id))
    #else:
        # should modifty this case!!!
        #return redirect(url_for('profile',id=current_user.id))

@app.route("/relation/add/<id>")
@login_required
def add_friend(id):
    # check the status between them first
    print(current_user.id)
    if current_user:
        status = service.relation.GetRelationStatus(current_user.id,int(id))
        # if not friends nor pending, then the status will be pending : 1 
        #if None, means there is no relation before, or the user doesn't exisit
        if status == None :
            # check if user is exist 
            user = service.user.GetUserById(id)
            if user:
                result = service.relation.UpdateRelation(current_user.id,int(id),1,current_user.id)
                result = "Pending"
            else:
                return "user doesn't exisit!!"
        # 0 means, was friends before, or was pending and rejectd    
        elif status == 0:
            result = service.relation.UpdateRelation(current_user.id,int(id),1,current_user.id)
            result = "Pending"
        elif status ==1 : 
            result = "Status is already pending!"
        elif status ==2:
             result = "We are friends!"
            
    
    return result


@app.route("/friends")
@login_required
def get_friends():
    # Get friends for id
    friends = ""
    friends = service.relation.GetFriends(current_user.id)
    Notfriends = service.relation.GetNotFriends(current_user.id)
    if current_user and friends:
        return render_template('friends.html',Notfriends=Notfriends,friends=friends,current_user=current_user)

    
@app.route("/profile/<id>/",methods=['GET', 'POST'])
@app.route("/profile/<id>/<img_url>",methods=['GET', 'POST'])
@login_required
def profile(id,img_url=None):
    friends = user = recentposts = status = userimageform = postform = relationform = None
    # Get the profile for the user using the Id
    user = service.user.GetUserById(int(id))
    # Check the friendship status
    
    if current_user:
        # get my friend's profile
        # if logged-in user's id is not the same as the profile id, it means not my profile
        if current_user.id != int(id): 
            relation = service.relation.GetRelation(current_user.id,int(id))
            if relation:
                if relation.status == 2:
                    status = "Friends"
                    # it means we are friends, so we get the friends list, and recent posts
                    friends = service.relation.GetFriends(int(id))
                    recentposts = service.post.Getlast10posts(int(id))
                    userimageform = UploadUserImageForm()
                    postform = PostForm()
                # if pending, and the action done by profile user id, then I can accept or not.
                elif relation.status == 1 and relation.action_by ==int(id):
                    status = "Accept/Delete"
                # if pending, and the action by me, then just show "Pending"
                elif relation.status == 1 and relation.action_by == current_user.id:
                    status = "Pending"
                    relationform = RelationForm()
                elif relation.status == 0:
                    status = "Add Friend"
            else:
                status = "Add Friend"
                relationform = RelationForm()
                if relationform.validate_on_submit():
                    if relationform.addfriend.data:
                        result = service.relation.UpdateRelation(current_user.id,int(id),1,current_user.id) 
                        status = "Pending"

            


        else:
            # it means this is my profile
            status = "Me"
            friends = service.relation.GetFriends(int(id))
            
            # show upload profile image form
            userimageform = UploadUserImageForm()
            postform = PostForm()
            if postform.validate_on_submit():
                if postform.postimage:
                    file = postform.postimage.data 
                    url = service.general.UploadImage(file)
                    newpost = service.post.AddPost(postform.text.data,current_user.id,url)
                
                else:
                    newpost = service.post.AddPost(postform.text.data,current_user.id)
                    
            recentposts = service.post.Getlast10posts(int(id))
  
    return render_template('user-profile.html',user = user,current_user = current_user,friends = friends,posts = recentposts,status=status,userimageform = userimageform,postform = postform,relationform=relationform)

@app.route("/test/load")
def load():
    result = test.loadtestdata()
    return result



@app.route("/like",methods=['POST'])
def like():   

    content = request.get_json()
    likes = service.post.LikePost(int(content['postid']))
    likes_obj = {}
    likes_obj["likes"] = likes
    likes_obj["postid"] = content['postid']
    json_data = json.dumps(likes_obj)
    return json_data

@app.route("/login", methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return main()
        #return render_template('index.html', title='home',current_user=current_user,newposts = GetRecentPosts(),userimageform = userimageform,postform = postform)

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            #session['currentuserid'] = user.id
            #session['currentusername'] = user.name
            #return render_template('index.html', title='home',currentuser=current_user,newposts = GetRecentPosts())
            return main()
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')


    return render_template('login2.html', title='Login', form=form)

def GetRecentPosts():
    #prcurrent_user.id
    newposts = service.post.GetNewPosts(current_user.id)
    return newposts

@app.route("/register", methods=['GET', 'POST'])    
def register():
    if current_user.is_authenticated:
        #return render_template('index.html', title='Login', form=form)
        return main()
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name = form.name.data, email = form.email.data,password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register2.html', title='Register', form=form)


@app.route("/logout")
def logout():
        logout_user()
        return redirect(url_for('login'))

@app.route("/updatestatus",methods=['POST'])
def updatestatus():   

    content = request.get_json()
    result = service.relation.UpdateRelation(current_user.id,int(content['userid']),int(content['status']),int(content['userid']))
    status_obj = {}
    status_obj["userid"] = content['userid']
    json_data = json.dumps(status_obj)
    return json_data



def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename) #pict name and itself
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        current_user.weight = form.weight.data
        current_user.city = form.city.data
        current_user.interest = form.interest.data
        current_user.languages = form.languages.data
        current_user.birthday = form.birthday.data
        db.session.commit()
        #'Your account has been updated!', 'success'
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.password.data = current_user.password
        current_user.weight = form.weight.data
        current_user.city = form.city.data
        current_user.birthday = form.birthday.data
    #image_file = url_for('static', filename='profile_pics/' + current_user.image_file) # I couldnt use it
    return render_template('account.html', title='Account',form=form)


