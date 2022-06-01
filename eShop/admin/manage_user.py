from flask import Blueprint, render_template, url_for, redirect, session, request, abort
from extention import mongodb_client

mng_user = Blueprint("manage-user", __name__, url_prefix="/manage-user", template_folder="templates", static_folder="static")


@mng_user.route("/", methods=['GET','POST'])
def manage_user():
    if "username" in session:
        users = mongodb_client.db.users
        all_user = users.find()
        return render_template("manage-user/manage-user.html", all_user=all_user, id = 0)
    else:
        return redirect(url_for("admin.adminLogin"))

@mng_user.route("/add-user", methods=['GET','POST'])
def add_user():
    if "username" in session:
        users = mongodb_client.db.users
        if request.method == "POST":
            full_name = request.form['Full_Name']
            email = request.form['Email']
            username = request.form['Username'] 
            password = request.form['Password']
            users.insert_one({"fullName":full_name,"email":email,"username":username,"password":password})
            return redirect(url_for('admin.manage-user.manage_user'))
        
        return render_template("manage-user/add-user.html")
    
    else:
        return redirect(url_for("admin.adminLogin"))

@mng_user.route("/update-user", methods=['GET','POST'])
def update_user():
    if "username" in session:
        username=request.args.get('username')
        user = mongodb_client.db.users
        current_user = user.find_one({"username":username})

        if request.method == "POST":
            full_name = request.form['Full_Name']
            email = request.form['Email']
            username = request.form['Username'] 

            user.find_one_and_update({"username": username}, {"$set": {"fullName":full_name,"email":email,"username":username}}, {"returnNewDocument": "true"})
            return redirect(url_for('admin.manage-user.manage_user'))
            
        return render_template("manage-user/update-user.html", current_user=current_user)

    else:
        return redirect(url_for("admin.adminLogin"))


@mng_user.route("/change-password", methods=['GET','POST'])
def change_password():
    if "username" in session:
        username=request.args.get('username')
        users = mongodb_client.db.users
        user = users.find_one({ "username" : username})
        if request.method == "POST":
            username = request.form['username']
            new_password = request.form['new_password']
            users.find_one_and_update({"username": username}, {"$set": {"password": new_password}}, {"returnNewDocument": "true"})
            return redirect(url_for('admin.manage-user.manage_user'))

        return render_template("manage-user/change-password.html", current_user=user)

    else:
        return redirect(url_for("admin.adminLogin"))


@mng_user.route("/delete/<username>")
def delete_user(username):
    if "username" in session:
        users = mongodb_client.db.users
        users.delete_one({"username": username})
        return redirect(url_for('admin.manage-user.manage_user'))
    else:
        return redirect(url_for("admin.adminLogin"))





                

