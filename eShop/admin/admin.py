from flask import Blueprint, render_template, url_for, redirect, session,request
from .manage_admin import mng_admn
from .manage_category import mng_ctgry
from .manage_items import mng_items
from .manage_order import mng_order
from .manage_user import mng_user
from extention import mongodb_client

admin = Blueprint('admin', __name__, template_folder="templates", static_folder="static")

admin.register_blueprint(mng_admn)
admin.register_blueprint(mng_ctgry)
admin.register_blueprint(mng_items)
admin.register_blueprint(mng_order)
admin.register_blueprint(mng_user)


@admin.route("/home", methods=['GET','POST'])
def adminHome():
       if "username" in session:
              return render_template("admin_home.html")
       else:
              return redirect(url_for("admin.adminLogin"))


@admin.route("/login", methods=['GET','POST'])
def adminLogin():
       admin = mongodb_client.db.admins
       if request.method == 'POST':
              print(request.form['username'])
              print(request.form['password'])
              user = admin.find_one({ "username" : request.form['username']})
              if user:
                     session['username'] = request.form['username']
                     return redirect(url_for("admin.adminHome"))
              else:    
                     return "<h1>username/passowrd incorrect</h1>"

       return render_template("admin_login.html")

@admin.route("/logout")
def adminLogout():
    session.clear()
    return redirect(url_for("admin.adminLogin"))


       # @admin.route("/signup", methods=['GET','POST'])
       # def adminRegister():
       #        eShop = mongodb_client.db.eShop
       #        if request.method == 'POST':
       #               print(request.form['username'])
       #               print(request.form['password'])
       #               existing_user = eShop.find_one({ "username" : request.form['username']})
       #               if existing_user :
       #                      return redirect(url_for("admin.adminLogin"))   
       #               else:
       #                      new_user = eShop.insert_one({ "username" : request.form['username'], "password": request.form['password'] })
       #                      return redirect(url_for("admin.adminLogin"))
       #        return render_template("admin_signup.html")

