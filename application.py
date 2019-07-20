from flask import Flask, render_template, request, url_for, redirect
from models import db
from config import *

application = app = Flask(__name__) # application variable is needed when deploy to AWS
app.config.from_object(DevelopmentConfig)
db.init_app(app)


import views,errors # adding all the routing from the views.py

if __name__ == '__main__':    
    app.config['TEMPLATES_AUTO_RELOAD'] = True      
    app.jinja_env.auto_reload = True
    app.run(debug=True)

    
    

