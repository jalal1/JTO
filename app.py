from flask import Flask
from models import db
import service.user

app = Flask(__name__)

POSTGRES = {
    'user': 'postgres',
    'pw': '1',
    'db': 'jto',
    'host': 'localhost',
    'port': '5432',
}

app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
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
