from application import app
import service.user
import service.post
import service.relation
from flask import render_template,request
from forms import PostForm


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