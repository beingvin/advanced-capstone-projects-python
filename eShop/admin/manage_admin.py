from flask import Blueprint, render_template, url_for, redirect, session, request, abort
from extention import mongodb_client

mng_admn = Blueprint("manage-admin", __name__, url_prefix="/manage-admin", template_folder="templates", static_folder="static")


@mng_admn.route("/", methods=['GET','POST'])
def manage_admin():
    if "username" in session:
        admins = mongodb_client.db.admins
        all_admin = admins.find()
        return render_template("manage-admin/manage-admin.html", all_admin=all_admin, id = 0)
    else:
        return redirect(url_for("admin.adminLogin"))

@mng_admn.route("/add-admin", methods=['GET','POST'])
def add_admin():
    if "username" in session:
        admins = mongodb_client.db.admins
        if request.method == "POST":
            full_name = request.form['Full_Name']
            username = request.form['Username'] 
            password = request.form['Password']
            admins.insert_one({"fullName":full_name,"username":username,"password":password})
            return redirect(url_for('admin.manage-admin.manage_admin'))
        
        return render_template("manage-admin/add-admin.html")
    
    else:
        return redirect(url_for("admin.adminLogin"))

@mng_admn.route("/update-admin", methods=['GET','POST'])
def update_admin():
    if "username" in session:
        username=request.args.get('username')
        admins = mongodb_client.db.admins
        current_admin = admins.find_one({"username":username})

        if request.method == "POST":
            username= request.form['username']
            new_full_name = request.form['new_full_name']  
            new_username = request.form['new_username']
            
            print(new_username)
            admins.find_one_and_update({"username": username}, {"$set": {"fullName":new_full_name,"username": new_username}}, {"returnNewDocument": "true"})
            return redirect(url_for('admin.manage-admin.manage_admin'))
            
        return render_template("manage-admin/update-admin.html", current_admin=current_admin)

    else:
        return redirect(url_for("admin.adminLogin"))


@mng_admn.route("/change-password", methods=['GET','POST'])
def change_password():
    if "username" in session:
        username=request.args.get('username')
        admins = mongodb_client.db.admins
        admin = admins.find_one({ "username" : username})

        if request.method == "POST":
            username = request.form['username']
            new_password = request.form['new_password']
            admins.find_one_and_update({"username": username}, {"$set": {"password": new_password}}, {"returnNewDocument": "true"})
            return redirect(url_for('admin.manage-admin.manage_admin'))

        return render_template("manage-admin/change-password.html", current_admin=admin)

    else:
        return redirect(url_for("admin.adminLogin"))


@mng_admn.route("/delete/<username>")
def delete_admin(username):
    if "username" in session:
        admins = mongodb_client.db.admins
        admins.delete_one({"username": username})
        return redirect(url_for('admin.manage-admin.manage_admin'))
    else:
        return redirect(url_for("admin.adminLogin"))





                

