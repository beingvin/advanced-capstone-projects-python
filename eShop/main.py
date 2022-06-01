from pprint import pprint
from venv import create
from flask import Blueprint, jsonify, render_template, url_for, redirect, session, request, flash,abort, json, current_app
from stripe_checkout.stripe_checkout import stripe_checkout
from cart.cart import mng_cart
from bson import ObjectId, json_util
from extention import mongodb_client


main = Blueprint("main", __name__, static_folder="static", template_folder="templates")

main.register_blueprint(stripe_checkout)
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
                print(cart_user['cartItems'])
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


@main.route("/addCart/<id>",  methods=['GET','POST'])
def addCart(id):

    if "username" in session:
        if request.method == "GET" :
        # id = request.args.get(id)
            id = id
            exesting_user = mongodb_client.db.cart.find_one({"username": session['username']})
            
            if exesting_user:

                if ObjectId(id) in exesting_user['cartItems']:
                    # return render_template('cart.html', cart = exesting_user)
                    return redirect(url_for("main.home"))   
                else:
                    appendId = mongodb_client.db.cart.update_one( {"username": session['username']},{ "$push" : {"cartItems": ObjectId(id) }})
                # return render_template('cart.html', cart = exesting_user)
                    session['cart'] = int(len(exesting_user['cartItems']) + 1)
                return redirect(url_for("main.home"))   

            else :  
                saveTocart = mongodb_client.db.cart.insert_one({"username": session['username'], "cartItems": [ObjectId(id)] }, )
                # return redirect(url_for("main.cart"))
                return redirect(url_for("main.home"))   

        return abort(404)
    else:
        return redirect(url_for("login"))   


@main.route("/cartItems",  methods=['GET','POST'])
def cartItems():

    if "username" in session:
        collection = mongodb_client.db.cart.find_one({"username": session['username']})

        cart_items = mongodb_client.db.cart.aggregate([{

                        "$lookup": {
                            "from":"items",
                            "localField":"cartItems",
                            "foreignField":"_id",
                            "as":"cartLists"
                        }
                    }])
        
        cart_lists = []
       

        for i in cart_items:
            # pprint(i["_id"])
            if i['username'] == session['username']:
                for items in i["cartLists"]:
                    cart_lists.append(items)

        def parse_json(data):
             return json.loads(json_util.dumps(data))

        cart_dict = { "username" : session['username'], "cart": cart_lists}

        if collection:
            # return render_template('cart.html', cart = cartLists)
            return  parse_json(cart_dict)
        else:
            return "something went wrong"

    else:
        return redirect(url_for("main.login"))  


@main.route("/viewCart",  methods=['GET','POST'])
def viewCart():
    if "username" in session:
        return render_template('cart.html')
    else:
        return redirect(url_for("main.login"))

@main.route("/deletItem",  methods=['GET','POST'])
def deletItem():
    id = request.args.get('id')
    if "username" in session:
        
        #delete item from db
        collection = mongodb_client.db.cart
        collection.find_one_and_update({"username": session['username']},{ "$pull" : {"cartItems": ObjectId(id) }})
        print("item deleted")

        # update cart button 
        exesting_user = collection.find_one({"username": session['username']})
        session['cart'] = int(len(exesting_user['cartItems']))

       
        return redirect(url_for('main.viewCart'))
    else:
         return redirect(url_for("main.login"))

@main.route("/signout")
def signout():
    session.pop('username')
    session.pop('cart')
    flash('successfully logged out')
    return redirect(url_for("main.login"))
