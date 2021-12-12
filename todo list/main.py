
from flask import Flask, render_template, request,url_for, redirect, flash, session, g 
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from sqlalchemy.orm import backref
from werkzeug.security import generate_password_hash, check_password_hash
from random_link_generator import random_link



SECREAT_KEY = "THISISSECREATKEY"
DB_URI = 'sqlite:///todo.db'

app = Flask(__name__)
app.config['SECRET_KEY'] = SECREAT_KEY

login_manager = LoginManager()
login_manager.init_app(app)


# CREATE DB
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# CREATE URL TABLE
class Url(db.Model):
    __tablename__ = "url"
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(50), unique=False, nullable=False)
    date_created= db.Column(db.String(15), unique = False, nullable = True)
    # ***************Parent Relationship*************#

    url_todo_lists = db.relationship("Todolist", backref = "url_lists")
    user_todo_lists = db.relationship("User", backref="user_lists")

# CREATE  USER TABLE
class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    date_created= db.Column(db.String(15), unique = False, nullable = True)
    # created_date =db.Column(db.Date(),
    #                        server_default = db.func.now())

    # ***************Child Relationship*************#
    url_id = db.Column(db.Integer, db.ForeignKey("url.id"))
    # user_lists = db.relationship("Url", backref="user_todo_lists")
    lists = db.relationship("Todolist", backref="userId")
  


# CREATE TODOLIST TABLE
class Todolist(db.Model):
    __tablename__="todolist"
    id=db.Column(db.Integer, primary_key = True)
    title=db.Column(db.String(100), unique = False, nullable = True)
    text=db.Column(db.String(1500), unique = False, nullable = True)
    # time_created=db.Column(db.DateTime(timezone=True),
    #                        server_default = db.func.now())
    # time_updated=db.Column(db.DateTime(timezone=True),
    #                        onupdate = db.func.now())

    date_created= db.Column(db.String(15), unique = False, nullable = True)
    date_updated= db.Column(db.String(15), unique = False, nullable = True)

    star=db.Column(db.Boolean, unique = False,
                   default = False,  nullable = True)
    color=db.Column(db.String(50), unique = False, nullable = True)
    user_id =db.Column(db.Integer, db.ForeignKey('user.id'))
    url_id = db.Column(db.Integer, db.ForeignKey('url.id'))

    # url_lists =db.relationship("Url", backref = "url_todo_lists")

# db.create_all()


# CREATE  USER LOADER
@ login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# CREATE  DYNAMIC FOOTER DATE
@app.context_processor
def inject_now():
    return {'footer_year': datetime.now().year, 'url':str(random_link)}


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session :
        all_user = User.query.all()
        user = [x for x in all_user if x.id == session['user_id']][0]
        g.user = user
        print(f"g user name : {g.user.email}")


########################################## ####### #### HOME ####
@ app.route("/", methods = ["GET", "POST"])
def index():
    url=str(random_link)
    return render_template("index.html", url=url)


########################################## ####### #### CREATE/READ ####
@ app.route("/new/<url>", methods = ["GET", "POST"])
def create_list(url):
    #### save url if not exist
    date = datetime.today().strftime("%d/%m/%Y")
    link = Url.query.filter_by(link=url).first() 
    if not link:
        new_link = Url(link=url, date_created=date)
        db.session.add(new_link)
        db.session.commit()
        return redirect(url_for("create_list", url=url))

    
    message=request.form.get("Message")
    star = request.form.get("Checkbox")    
    color_tag=""
    user=current_user

    #### if user is athenticated show users lists 
    if current_user.is_authenticated:
        username=User.query.filter_by(id = user.id).first()
        lists=username.lists
        if request.method == "POST":
            new_list=Todolist(text = message, color = color_tag, star=star , user_id = user.id, url_id=link.id, date_created=date)
            db.session.add(new_list)
            db.session.commit()
            return redirect(url_for("create_list", url=url))
        return render_template("lists.html", todo_title = date, lists = lists)

    #### if user is not athenticated show url lists 
    else:
        lists=Todolist.query.filter_by(url_id = link.id).all()
        if request.method == "POST":
            new_list=Todolist(text = message, color = color_tag, star=star, url_id=link.id, date_created=date )
            db.session.add(new_list)
            db.session.commit()
            return redirect(url_for("create_list", url=url))
        return render_template("lists.html", todo_title= date , lists = lists)



########################################## ####### #### UPDATE ####
@ app.route("/update/<int:list_id>")
def update_list(list_id):
    return "<h1>You clicked updated</>"

########################################## ####### #### DELETE ####
@ app.route("/delete/<int:list_id>", methods = ["GET"])
def delete_list(list_id):
    url=request.args["title"]
    list=db.session.query(Todolist).get(list_id)
    if list:
        db.session.delete(list)
        db.session.commit()
        return redirect(url_for("create_list", url=url))
    else:
        return '<h1>something went wrong</h1>'


########################################## ####### #### SIGNUP ####
@ app.route('/user/signup/<url>', methods = ["POST", "GET"])
def signup(url):
    link = Url.query.filter_by(link=url).first()
    if request.method == "POST":

        if User.query.filter_by(email = request.form.get('email')).first():
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password=generate_password_hash(
            request.form.get('password'),
            method = 'pbkdf2:sha256',
            salt_length = 8
        )
        new_user = User(
            email=request.form.get('email'),
            password=hash_and_salted_password,
            date_created = datetime.today().strftime("%d/%m/%Y"),
            url_id=link.id
            
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("login"))

    return render_template("signup.html", logged_in=current_user.is_authenticated)



########################################## ####### #### LOGIN ####
@app.route("/user/login", methods=["POST", "GET"])
def login():
    url = str(random_link)
    if request.method == "POST":
        session.pop('user_id', None)
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        # Email doesn't exist or password incorrect.       
        if not user:
            flash("This user doesn't exist, please try again.")
            return redirect(url_for("login"))
        elif not check_password_hash(user.password, password):
            flash("password incorrect, please try again.")
            return redirect(url_for('login'))
        else:
            login_user(user)
            flash("login successful")
            session['user_id'] = user.id
            print(f"session id is : { session['user_id'] }")
            return redirect(url_for("create_list", url=url ))

    return render_template("login.html",logged_in=current_user.is_authenticated)


########################################## ####### #### LOGOUT ####
@app.route('/logout')
@login_required
def logout():
    # if not g.user:
    #      return redirect(url_for("login"))
    logout_user()
    flash("Logout successful")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
