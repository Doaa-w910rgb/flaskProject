from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
# from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'WNkYdsV2xKNZBXZQEsAAlweq781SWrOl23Pm'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
# migrate = Migrate(app, db)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


from flasktasks import routes
from flasktasks.routes import users
from flasktasks.models import User
from flasktasks.routes import posts


app.register_blueprint(posts)






    

    