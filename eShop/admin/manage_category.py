from email.mime import image
from flask import Blueprint, render_template, url_for, redirect, session, request, abort, current_app
from extention import mongodb_client
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
import os

mng_ctgry = Blueprint("manage-category", __name__, url_prefix="/manage-category", template_folder="templates", static_folder="static")


@mng_ctgry.route("/", methods=['GET','POST'])
def manage_category():
    if "username" in session:
        categories = mongodb_client.db.categories
        all_categories = categories.find()
        return render_template("manage-category/manage-category.html", all_categories=all_categories)
    else:
        return redirect(url_for("admin.adminLogin"))

@mng_ctgry.route("/add-category", methods=['GET','POST'])
def add_category():
    if "username" in session:

        categories = mongodb_client.db.categories

        if request.method == "POST":
            title = request.form['title']
            image = request.files['image']
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER_CTGRY'], secure_filename(image.filename)))
            image_link = image.filename
            image_link = request.form['imageLink']
            featured = request.form['featured']
            active = request.form['active']
            categories.insert_one({"title":title, "imageLink": image_link, "featured":featured, "active":active})
            return redirect(url_for('admin.manage-category.manage_category'))
        
        return render_template("manage-category/add-category.html")

    else:
        return redirect(url_for("admin.adminLogin"))

@mng_ctgry.route("/update-category", methods=['GET','POST'])
def update_category():
    if "username" in session:
        id=request.args.get('id')
        categories = mongodb_client.db.categories
        current_category = categories.find_one({"_id": ObjectId(id)})
        if request.method == "POST":
            title = request.form['title']
            image_link = request.form['imageLink']
            featured = request.form['featured'] 
            active = request.form['active']
            categories.find_one_and_update({"_id": ObjectId(id)}, {"$set": {"title": title,"featured": featured ,"imageLink": image_link,"active":active}}, {"returnNewDocument": "true"})
            return redirect(url_for("admin.manage-category.manage_category"))
        
        return render_template("manage-category/update-category.html", current_category=current_category)
    else:
        return redirect(url_for("admin.adminLogin"))



@mng_ctgry.route("/delete/<id>")
def delete_category(id):
    if "username" in session:
        categories = mongodb_client.db.categories
        categories.delete_one({"_id":ObjectId(id)})
        return redirect(url_for("admin.manage-category.manage_category"))
    else:
        return redirect(url_for("admin.adminLogin"))



