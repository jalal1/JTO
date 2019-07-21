from application import app, db, bcrypt, login_manager
import service.user
import service.post
import service.relation
from flask import render_template,request,url_for, flash, redirect
from forms import PostForm, RegistrationForm,LoginForm
from models import User, Post
from flask_login import login_user, current_user, logout_user




@app.route("/")
def main():

    return render_template('index.html')



@app.route("/user/add/<name>/<email>")
def add_user(name,email):
    result = service.user.AddUser(name,email)
    return result


@app.route("/user/<id>")
def get_user(id):
    result = service.user.GetUserById(int(id))
    return result.name


@app.route("/post/add/<text>")
def add_post(text):
    result = service.post.AddPost(text)
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

@app.route("/relation/add/<id1>/<id2>")
def add_friend(id1,id2):
    # When add a friend, the status is pending
    result = service.relation.UpdateRelation(int(id1),int(id2),2,int(id1))
    return result

@app.route("/friends/<id>")
def get_friends(id):
    # Get friends for id
    friends = service.relation.GetFriends(int(id))
    users = service.relation.GetAll(id)
    return render_template('friends.html',friends=friends,users=users,user=id)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return render_template('index.html')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            return render_template('index.html', title='home', form=form)
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login2.html', title='Login', form=form)


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