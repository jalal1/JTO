from flask import Flask
from models import db # problem here
from config import *
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from models import User

application = app = Flask(__name__) # application variable is needed when deploy to AWS
app.config.from_object(ProductionConfig)
db.init_app(app)
bcrypt = Bcrypt(app) # to encrypt passwords

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
     return User.query.get(user_id)


import views,errors # adding all the routing from the views.py

if __name__ == '__main__':    
    #app.config['TEMPLATES_AUTO_RELOAD'] = True    # added to config file  
    app.jinja_env.auto_reload = True
    #app.run(debug=True)
    app.run()

    
    

