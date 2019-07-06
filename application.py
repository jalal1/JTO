from flask import Flask
from models import db
import service.user,service.post
from config import *

application = app = Flask(__name__) # application variable is needed when deploy to AWS
app.config.from_object(DevelopmentConfig)
db.init_app(app)


@app.route("/")
def main():

    return "Hello World!"

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

if __name__ == '__main__':
    app.run()
