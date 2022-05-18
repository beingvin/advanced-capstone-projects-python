from flask import Blueprint, render_template, url_for, redirect, session, request, abort
from extention import mongodb_client
from bson.objectid import ObjectId

mng_ctgry = Blueprint("manage-category", __name__, url_prefix="/manage-category", template_folder="templates", static_folder="static")


@mng_ctgry.route("/", methods=['GET','POST'])
def manage_category():
    categories = mongodb_client.db.categories
    all_categories = categories.find()
    return render_template("manage-category/manage-category.html", all_categories=all_categories)

@mng_ctgry.route("/add-category", methods=['GET','POST'])
def add_category():
    categories = mongodb_client.db.categories
    if request.method == "POST":
        title = request.form['title']
        featured = request.form['featured'] 
        active = request.form['active']
        categories.insert_one({"title":title, "imageLink": "#", "featured":featured, "active":active})
        return redirect(url_for('admin.manage-category.manage_category'))
    return render_template("manage-category/add-category.html")

@mng_ctgry.route("/update-category", methods=['GET','POST'])
def update_category():
    id=request.args.get('id')
    categories = mongodb_client.db.categories
    current_category = categories.find_one({"_id": ObjectId(id)})
    if request.method == "POST":
        title = request.form['title']
        featured = request.form['featured'] 
        active = request.form['active']
        print(title)
        print(featured)
        print(active)
        print(id)
        categories.find_one_and_update({"_id": ObjectId(id)}, {"$set": {"title": title,"featured": featured ,"active":active}}, {"returnNewDocument": "true"})
        print("updated")
        return redirect(url_for("admin.manage-category.manage_category"))
       
    return render_template("manage-category/update-category.html", current_category=current_category)



@mng_ctgry.route("/delete/<id>")
def delete_category(id):
    print(ObjectId(id))   
    categories = mongodb_client.db.categories
    categories.delete_one({"_id":ObjectId(id)})
    return redirect(url_for("admin.manage-category.manage_category"))



