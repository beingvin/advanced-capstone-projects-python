from flask import Blueprint, render_template, url_for, redirect, session, request, abort
from extention import mongodb_client
from bson.objectid import ObjectId

mng_items = Blueprint("manage-items", __name__, url_prefix="/manage-items", template_folder="templates", static_folder="static")


@mng_items.route("/", methods=['GET','POST'])
def manage_items():
    if "username" in session:
        items = mongodb_client.db.items
        items = items.find()
        return render_template("manage-items/manage-items.html", items=items)
    else:
              return redirect(url_for("admin.adminLogin"))

@mng_items.route("/add-items", methods=['GET','POST'])
def add_items():
    if "username" in session:
        items = mongodb_client.db.items
        categories = mongodb_client.db.categories
        all_categories =  categories.find()
        print(categories)
        if request.method == "POST":
            title = request.form['title']
            image_link = request.form['imageLink']
            price = request.form['price']
            brand = request.form['brand']
            # size = [request.form.getlist('S'),request.form.getlist ('M'),request.form.getlist('L'),request.form.getlist('XL'),request.form.getlist('XXL'),request.form.getlist('XXXL')]
            size = request.form.getlist('size')
            description = request.form['description']
            material = request.form['material']
            type = request.form['type']
            gender = request.form['gender']
            category = request.form['category']
            occasion = request.form['occasion']
            featured = request.form['featured'] 
            active = request.form['active']
            items.insert_one({"title":title, "imageLink":image_link, "price":price,"brand":brand,"size":size, "productDetails" : {"descripation": description, "material":material,"type":type, "gender":gender, "category": category, "occasion":occasion } ,"featured":featured, "active":active})
            return redirect(url_for('admin.manage-items.manage_items'))
        
        return render_template("manage-items/add-items.html",  all_categories= all_categories)

    else:
        return redirect(url_for("admin.adminLogin"))

@mng_items.route("/update-items", methods=['GET','POST'])
def update_items():
    if "username" in session:
        id=request.args.get('id')
        items = mongodb_client.db.items
        current_item = items.find_one({"_id": ObjectId(id)})
        categories = mongodb_client.db.categories
        all_categories =  categories.find()
        if request.method == "POST":
            title = request.form['title']
            image_link = request.form['imageLink']
            price = request.form['price']
            brand = request.form['brand']
            # size = [request.form['S'],request.form['M'],request.form['L'],request.form['XL'],request.form['XXL'],request.form['XXXL']]
            size = request.form.getlist('size')
            print(size)
            description = request.form['description']
            material = request.form['material'] 
            type = request.form['type']
            gender = request.form['gender']
            category = request.form['category']
            occasion = request.form['occasion']
            featured = request.form['featured'] 
            active = request.form['active']
            print(id)
            items.find_one_and_update({"_id": ObjectId(id)}, {"$set": {"title":title, "imageLink": image_link, "price":price,"brand":brand,"size":size, "productDetails" : {"descripation": description, "material":material,"type":type, "gender":gender,"category" :category, "occasion":occasion } ,"featured":featured, "active":active}}, {"returnNewDocument": "true"}) 
            return redirect(url_for("admin.manage-items.manage_items"))
        return render_template("manage-items/update-items.html", current_item=current_item, all_categories= all_categories)
    else:
        return redirect(url_for("admin.adminLogin"))


@mng_items.route("/delete/<id>")
def delete_items(id):
    if "username" in session:
        items = mongodb_client.db.items
        items.delete_one({"_id":ObjectId(id)})
        return redirect(url_for("admin.manage-items.manage_items"))
    else:
        return redirect(url_for("admin.adminLogin"))


