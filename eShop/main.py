from flask import Blueprint, render_template, url_for, redirect, session, request
from extention import mongodb_client

main = Blueprint("main", __name__, static_folder="static", template_folder="templates")



##################### Create route #####################

@main.route("/")
def home():
    if "username" in session:
       return render_template('home.html', username = session['username'])
    else:
       return render_template('index.html')



@main.route("/login", methods=['GET','POST'])
def login():
    user = mongodb_client.db.users
    if request.method == 'POST':
        print(request.form['username'])
        print(request.form['password'])
        user = user.find_one({ "username" : request.form['username']})
        if user:
            session['username'] = request.form['username']
            return redirect(url_for("main.home"))
        else:    
           return "<h1>username/passowrd incorrect</h1>"
    return render_template('registration/login.html')
   
@main.route("/signup", methods=['GET','POST'])
def signup():
    user = mongodb_client.db.users
    if request.method == 'POST':
            print(request.form['username'])
            print(request.form['password'])
            existing_user = user.find_one({ "username" : request.form['username']})
            if existing_user :
                return redirect(url_for("login"))   
            else:
                new_user = user.insert_one({ "username" : request.form['username'], "password": request.form['password'] })
                return redirect(url_for("login"))
    return render_template('registration/signup.html')     


@main.route("/items")
def items():
    if "username" in session:
       return render_template('items.html', username = session['username'])
    else:
       return render_template('index.html')
   


@main.route("/all_products")
def all_products():
    return render_template('all_products.html')


@main.route("/popular_items")
def popular_items():
    return render_template('popular_items.html')


@main.route("/new_arrivals")
def new_arrivals():
    return render_template('new_arrivals.html')


@main.route("/signout")
def signout():
    session.clear()
    return redirect(url_for("main.login"))
