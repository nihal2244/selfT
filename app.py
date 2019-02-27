from flask import Flask, render_template,request,redirect,url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from models.db import db
from models.user import User
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# db-config
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:qweasd@localhost/selftdb'
db.init_app(app)


# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"




# index
@app.route("/")

def index():
    return render_template('index.html')


# signUp
@app.route("/signup",methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        username = request.form.get('username', "").strip()
        email = request.form.get('email', "").strip()
        pwd = request.form.get('pwd', "").strip()
    
        if username=="" or email=="" or pwd == "": 
            print("some thing wrong with your email,password or user name")
        else:
            new_acc=User(username, email, pwd)
            db.session.add(new_acc)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('signup.html')



# login
@app.route('/login', methods=['GET', 'POST'])
def login():

    form = UserLoginForm(request.form)
    error = None
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(username=username.lower()).first()
        if user:
            if login_user(user):
                current_app.logger.debug('Logged in user %s', user.username)
                return redirect(url_for('secret'))
        error = 'Invalid username or password.'
    return render_template('login.html', form=form, error=error)

#home
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html')


#logout
@app.route('/logout', methods=['GET'])

def logout():
    logout_user()
    return redirect(url_for('login'))






if __name__ == "__main__":
    app.run(debug=True)
