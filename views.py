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
    user = newposts = ""
    user = get_user(1)
    if user:
        session['currentuserid'] =  user.id
        session['currentusername'] = user.name

    # Get friends posts
    if session.get('currentuserid'):
        newposts = service.post.GetNewPosts(int(session['currentuserid']),session['currentusername'])
    

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