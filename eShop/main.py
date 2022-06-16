from pprint import pprint
from flask import Blueprint, render_template, url_for, redirect, session, request, flash
from cart.cart import mng_cart
from extention import mongodb_client

import os



main = Blueprint("main", __name__, static_folder="static", template_folder="templates")

main.register_blueprint(mng_cart)


##################### Create route #####################

@main.route("/")
def home():
    if "username" in session:
        if "cart" in session:
            cart_user = mongodb_client.db.cart.find_one({"username": session['username']})
            session['cart'] = int(len(cart_user['cartItems']))
        else:
            cart_user = mongodb_client.db.cart.find_one({"username": session['username']})
            if cart_user:
                session['cart'] = int(len(cart_user['cartItems']))
            else:
                add_cart_user = mongodb_client.db.cart.insert_one ({"username": session['username'],"cartItems":[]})
                cart_user = mongodb_client.db.cart.find_one({"username": session['username']})
                session['cart'] = int(len(cart_user['cartItems']))
                print('cart user added')

    #    if exesting_user['cartItems'] == None:
    #       session['cart'] = 0
    #    else:   
    #       session['cart'] = int(len(exesting_user['cartItems']))

        categories = mongodb_client.db.categories.find()
        items = mongodb_client.db.items.find()
        
        return render_template('home.html', categories=categories, items=items)
    else:
        return render_template('index.html')

@main.route("/items")
def items():
    if "username" in session:

       return render_template('items.html')
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


@main.route("/login", methods=['GET','POST'])
def login():
    user = mongodb_client.db.users
    if request.method == 'POST':
        username = request.form['username'] 
        password = request.form['password']
        email = user.find_one({ "email" : username })
        user = user.find_one({ "username" : username,}) 
        if user or email :
            if user:
                if user['password'] == password :                    
                    session['username'] = user['email']
                    flash('successfully logged in')
                    return redirect(url_for("main.home"))
                else:
                    flash('password incorrect') 
                    return  render_template('registration/login.html')
            elif email:
                if email['password'] == password:
                    session['username'] = email['email']
                    flash('Logged in successfully')
                    return redirect(url_for("main.home"))
                else: 
                    flash('passowrd incorrect')
                    return render_template('registration/login.html')
        else:
           flash('username incorrect')  
           return render_template('registration/login.html')
    return render_template('registration/login.html')
    
   
@main.route("/signup", methods=['GET','POST'])
def signup():
    user = mongodb_client.db.users
    if request.method == 'POST':
            full_name = request.form['full_name']
            email = request.form['email']
            username = request.form['username'] 
            password = request.form['password']
            existing_user = user.find_one({ "username" : username})
            if existing_user :
                return redirect(url_for("login"))   
            else:
                new_user = user.insert_one({"fullName":full_name,"email":email,"username":username,"password":password})
                return redirect(url_for("main.login"))
    return render_template('registration/signup.html')


@main.route("/signout")
def signout():
    session.pop('username')
    session.pop('cart')
    flash('successfully logged out')
    return redirect(url_for("main.login"))
