from application import app
import service.user
import service.post
from flask import render_template,request
from forms import PostForm


@app.route("/")
def main():

    return render_template('index.html')


@app.route("/user/add/<email>")
def add_user(email):
    result = service.user.AddUser(email)
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