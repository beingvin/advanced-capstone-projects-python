from flask import Blueprint, render_template, url_for, redirect, session, request, abort
from extention import mongodb_client

mng_admn = Blueprint("manage-admin", __name__, url_prefix="/manage-admin", template_folder="templates", static_folder="static")


@mng_admn.route("/", methods=['GET','POST'])
def manage_admin():
    admins = mongodb_client.db.admins
    all_admin = admins.find()
    return render_template("manage-admin/manage-admin.html", all_admin=all_admin, id = 0)

@mng_admn.route("/add-admin", methods=['GET','POST'])
def add_admin():
    admins = mongodb_client.db.admins
    if request.method == "POST":
        full_name = request.form['Full_Name']
        username = request.form['Username'] 
        password = request.form['Password']
        admins.insert_one({"fullName":full_name,"username":username,"password":password})
        return redirect(url_for('admin.manage-admin.manage_admin'))
       
    return render_template("manage-admin/add-admin.html")


@mng_admn.route("/update-admin", methods=['GET','POST'])
def update_admin():
    username=request.args.get('username')
    admin = mongodb_client.db.admins
    current_admin = admin.find_one({"username":username})

    if request.method == "POST":
        new_username = request.form['username'] 
        print(new_username)
        admin.find_one_and_update({"username": username}, {"$set": {"username": new_username}}, {"returnNewDocument": "true"})
        return redirect(url_for('admin.manage-admin.manage_admin'))
       
    return render_template("manage-admin/update-admin.html", current_admin=current_admin)


@mng_admn.route("/change-password", methods=['GET','POST'])
def change_password():
    username=request.args.get('username')
    eShop = mongodb_client.db.eShop
    user = eShop.find_one({ "username" : username})
    password = user['password']
    print(user["password"])
    if request.method == "POST":
        new_password = request.form['new_password']
        eShop.find_one_and_update({"username": username}, {"$set": {"password": new_password}}, {"returnNewDocument": "true"})
        return redirect(url_for('admin.manage-admin.manage_admin'))
    return render_template("manage-admin/change-password.html", current_password=password)


@mng_admn.route("/delete/<username>")
def delete_admin(username):
    admins = mongodb_client.db.admins
    admins.delete_one({"username": username})
    return redirect(url_for('admin.manage-admin.manage_admin'))





                

