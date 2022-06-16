from flask import current_app, render_template, url_for, request, abort, Blueprint, session, redirect, json, jsonify
from .stripe_checkout.stripe_checkout import stripe_mng 
from extention import mongodb_client
from bson import ObjectId, json_util

mng_cart = Blueprint("mng_cart", __name__, url_prefix="cart", static_url_path="static_folder", static_folder="static", template_folder="templates")

mng_cart.register_blueprint(stripe_mng)


@mng_cart.route("/")
def home ():
    return {"name":"Manage cart"}


@mng_cart.route("/addCart/<id>",  methods=['GET','POST'])
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


@mng_cart.route("/cartItems",  methods=['GET','POST'])
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


@mng_cart.route("/viewCart",  methods=['GET','POST'])
def viewCart():
    if "username" in session:
        return render_template('cart.html')
    else:
        return redirect(url_for("main.login"))

@mng_cart.route("/deletItem",  methods=['GET','POST'])
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

       
        return redirect(url_for('main.mng_cart.viewCart'))
    else:
         return redirect(url_for("main.login"))
