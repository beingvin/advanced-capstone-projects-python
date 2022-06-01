from flask import Blueprint, render_template, url_for, redirect, session, request, abort
from extention import mongodb_client
from bson.objectid import ObjectId

mng_order = Blueprint("manage-order", __name__, url_prefix="/manage-order", template_folder="templates", static_folder="static")


@mng_order.route("/", methods=['GET','POST'])  
def manage_order():
    if "username" in session:
        items = mongodb_client.db.items
        items = items.find()
        return render_template("manage-order/manage-order.html")
    else:
              return redirect(url_for("admin.adminLogin"))