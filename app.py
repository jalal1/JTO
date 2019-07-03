from flask import Flask
from models import db,User

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

    result = AddUser()
    return result

def AddUser():
    error = "Error occured"
    try:
        user = User()
        user.id = 2 
        user.name = 'Jalal'
        user.email = 'jalalk111@uab.edu'
        user.password = '1'
        db.session.add(user)
        db.session.commit()
        return "User added successfully!!"
    except:
        return error
    return error



if __name__ == '__main__':
    app.run()