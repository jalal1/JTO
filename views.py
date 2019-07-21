from application import app, db, bcrypt, login_manager
import service.user
import service.post
import service.relation
import json
import test
from flask import render_template,request,url_for, flash, redirect,session
from forms import PostForm, RegistrationForm,LoginForm
from models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
def main():
<<<<<<< HEAD
    return render_template('index.html')
=======

    return redirect(url_for('login'))
>>>>>>> 28f6d2430b8ab99ef9c65aa8572872f6a4ee3cc5

@app.route("/search",methods=['POST'])
def search():   
    users = []
    content = request.get_json()
    result = service.user.Search(content['text'])
    for user in result:
        users.append(user.name)
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


@app.route("/post/add/<text>/<userid>")
def add_post(text,userid):
    result = service.post.AddPost(text,userid)
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
        service.post.UploadImage(file)
    return render_template('upload.html', title='Upload image', form=form)

@app.route("/relation/add/<id>")
def add_friend(id):
    # check the status between them first
    if session['currentuserid']:
        status = service.relation.GetRelationStatus(int(session['currentuserid']),int(id))
        # if not friends nor pending, then the status will be pending : 1 
        if status == 0 :
            result = service.relation.UpdateRelation(int(session['currentuserid']),int(id),1,int(session['currentuserid']))
            result = "Pending"
        elif status ==1 : 
            result = "Status is already pending!"
        elif status ==2:
             result = "We are friends!"
            
    
    return result


@app.route("/friends/<id>")
def get_friends(id):
    # Get friends for id
    friends = service.relation.GetFriends(int(id))
    return render_template('friends.html',friends=friends)

    
@app.route("/profile/<id>")
def profile(id):
    friends = user = recentposts = status =   ""
    # Get the profile for the user using the Id
    user = service.user.GetUserById(int(id))
    # Check the friendship status
    
    if session.get('currentuserid'):
        # get my friend's profile
        # if logged-in user's id is not the same as the profile id, it means not my profile
        if int(session.get('currentuserid')) != int(id): 
            relation = service.relation.GetRelation(int(session['currentuserid']),int(id))
            if relation:
                if relation.status == 2:
                    status = "Friends"
                    # it means we are friends, so we get the friends list, and recent posts
                    friends = service.relation.GetFriends(int(id))
                    recentposts = service.post.Getlast10posts(int(id))
                # if pending, and the action done by profile user id, then I can accept or not.
                elif relation.status == 1 and relation.action_by ==id:
                    status = "Accept/Delete"
                # if pending, and the action by me, then just show "Pending"
                elif relation.status == 1 and relation.action_by == int(session['currentuserid']):
                    status = "Pending"
                elif relation.status == 0:
                    status = "Add Friend"
            else:
                status = "No Relation!"
                


        else:
            # it means this is my profile
            status = "Me"
            friends = service.relation.GetFriends(int(id))
            recentposts = service.post.Getlast10posts(int(id))
                
    return render_template('user-profile.html',user = user,friends = friends,posts = recentposts,status=status)

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
    users = service.relation.GetAll(id)
    return render_template('friends.html',friends=friends,users=users,user=id)

@app.route("/login", methods=['GET', 'POST'])
def login():
<<<<<<< HEAD
    #if current_user.is_authenticated:
        #return render_template('index.html')
=======
    
    if current_user.is_authenticated:
        return render_template('index.html')
>>>>>>> 28f6d2430b8ab99ef9c65aa8572872f6a4ee3cc5
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            session['currentuserid'] = user.id
            session['currentusername'] = user.name

            return render_template('index.html', title='home',user="" ,form=form,currentuser = user,newposts = GetRecentPosts())
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login2.html', title='Login', form=form)

def GetRecentPosts():
    #print(session['currentuserid'])
    newposts = service.post.GetNewPosts(current_user.id,current_user.name)
    return newposts

@app.route("/register", methods=['GET', 'POST'])    
def register():
    if current_user.is_authenticated:
        return render_template('index.html', title='Login', form=form)
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
        return render_template('index.html')
<<<<<<< HEAD

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account', form=form)
=======
>>>>>>> 28f6d2430b8ab99ef9c65aa8572872f6a4ee3cc5
