from flask import Flask
from models import db
import service.user,service.post
from config import *


application = app = Flask(__name__) # application variable is needed when deploy to AWS
app.config.from_object(DevelopmentConfig)
db.init_app(app)

import views # adding all the routing from the views.py


if __name__ == '__main__':
    app.run()
