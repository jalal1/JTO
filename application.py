from flask import Flask
from models import db
import service.user
from config import *

application = app = Flask(__name__) # application name is needed when deploy to AWS
app.config.from_object(ProductionConfig)
db.init_app(app)


@app.route("/")
def main():

    return "Hello World!"

@app.route("/user/add")
def add_user():
    result = service.user.AddUser(4,'333333 @sdfsd.com')
    return result


@app.route("/user/<id>")
def get_user(id):
    result = service.user.GetUserById(int(id))
    return result.name


if __name__ == '__main__':
    app.run()
