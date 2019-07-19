from application import app
import service.user
import service.post
import service.relation
from flask import render_template,request,session
from forms import PostForm
import json
import test



@app.route("/")
def main():
    #supppose that user [9] is logged in
    user = get_user(9)
    if user:
        session['currentuserid'] = user.id
        session['currentusername'] = user.name

    # Get friends posts
    if session.get('currentuserid'):
        newposts = service.post.GetNewPosts(int(session['currentuserid']))

    return render_template('index.html',currentuser = user,newposts = newposts)

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
    return result


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

@app.route("/relation/add/<id1>/<id2>")
def add_friend(id1,id2):
    # When add a friend, the status is pending
    result = service.relation.UpdateRelation(int(id1),int(id2),2,int(id1))
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
        status = service.relation.GetRelation(int(session['currentuserid']),int(id))
    # if friends : get friends list and recent posts. 
    if status == 2:
        friends = service.relation.GetFriends(int(id))
        recentposts = service.post.Getlast10posts(id)
    # else : show user name, button with status, either "add friend" or "pending"
    return render_template('user-profile.html',user = user,friends = friends,posts = recentposts,status=status)

@app.route("/test/load")
def load():
    result = test.loadtestdata()
    return result
