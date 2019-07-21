from flask import Flask
from models import db # problem here
from config import *
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

application = app = Flask(__name__) # application variable is needed when deploy to AWS
app.config.from_object(DevelopmentConfig)
db.init_app(app)
bcrypt = Bcrypt(app) # to encrypt passwords

login_manager = LoginManager(app) 
login_manager.init_app(app)

import views,errors # adding all the routing from the views.py




if __name__ == '__main__':
    app.run()
