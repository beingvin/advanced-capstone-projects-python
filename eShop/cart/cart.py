from flask import current_app, render_template, url_for, request, abort, Blueprint, session

mng_cart = Blueprint("mng_cart", __name__, static_folder="static", template_folder="templates", url_prefix="cart")


@mng_cart.route("/")
def home ():
    return {"name":"Manage cart"}  
