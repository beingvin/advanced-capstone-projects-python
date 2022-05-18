from pydoc import describe
from flask import Blueprint, render_template, url_for, redirect, session, request, abort
from extention import mongodb_client
from bson.objectid import ObjectId

mng_items = Blueprint("manage-items", __name__, url_prefix="/manage-items", template_folder="templates", static_folder="static")


@mng_items.route("/", methods=['GET','POST'])
def manage_items():
    items = mongodb_client.db.items
    items = items.find()
    return render_template("manage-items/manage-items.html", items=items)

@mng_items.route("/add-items", methods=['GET','POST'])
def add_items():
    items = mongodb_client.db.items
    if request.method == "POST":
        title = request.form['title']
        price = request.form['price']
        brand = request.form['brand']
        size = [request.form['S'],request.form['M'],request.form['L'],request.form['XL'],request.form['XXL'],request.form['XXXL']]
        description = request.form['description']
        material = request.form['material']
        type = request.form['type']
        gender = request.form['gender']
        occasion = request.form['occasion']
        featured = request.form['featured'] 
        active = request.form['active']

        print(title)
        print(price)
        print(brand)
        print(size)
        print(description)
        print(material)
        print(type)
        print(gender)
        print(occasion)
        print(featured)
        print(active)

        items.insert_one({"title":title, "imageLink": "#", "price":price,"brand":brand,"size":size, "productDetails" : {"descripation": description, "material":material,"type":type, "gender":gender, "occasion":occasion } ,"featured":featured, "active":active})
        return redirect(url_for('admin.manage-items.manage_items'))

    return render_template("manage-items/add-items.html")
