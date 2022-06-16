from flask import Flask
from extention import mongodb_client
from admin.admin import admin
from main import main


##################### create app #####################
app = Flask(__name__)

app.config.from_pyfile("config.py")


##################### add database (mongodb_client) #####################
   
mongodb_client.init_app(app)


##################### register blueprints #####################

app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(main, url_prefix="")



if __name__ == "__main__":
   app.run(debug=True)

