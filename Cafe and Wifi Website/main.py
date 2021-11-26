from flask import Flask, render_template,url_for, redirect, jsonify, request
from flask.helpers import flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, form
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy
import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
app.secret_key = "TopSecretAPIKey"

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Cafe TABLE Configuration/Model
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    # convert to json
    def to_dict(self):
        dictionary = {}
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

# Create cafe form
class CafeForm(FlaskForm):
    name = StringField('Cafe Name', validators=[DataRequired()])
    location = StringField('Cafe Location ', validators=[DataRequired()])
    map_url = StringField('Cafe On Google map (URL)', validators=[
                           URL(message='Enter a valid URL')])
    img_url = StringField('Cafe Image (URL)', validators=[
                           URL(message='Enter a valid URL')])
    seats =StringField('How Many Seats Available', validators=[DataRequired()])
    coffee_price = StringField('Coffee Price', validators=[DataRequired()])
    has_toilet = BooleanField('Cafe has toilet ')
    has_wifi = BooleanField('Cafe has wifi ')
    has_sockets = BooleanField('Cafe has sockets ')
    can_take_calls = BooleanField('Allowed take calls')
    submit = SubmitField('Submit')

@app.context_processor
def inject_now():
    year = datetime.datetime.now().year
    # return render_template('base.html', footer_year=year )
    return {'footer_year': datetime.datetime.now().year}

########################################## Home route
@app.route('/')
def home():
    cafename = "Cafe hub"
    return render_template("home.html", cafename=cafename)



# @app.route('/base')
# def base():
#     year = datetime.datetime.now().year
#     return render_template ('base.html', footer_year=year)



########################################## Read Record


@app.route('/caffee-list')
def cafe_list():
    cafes = db.session.query(Cafe).all()
    print(cafes[0].name)
    return render_template("cafe_list.html", all_cafe=cafes)

########################################## Create Record
@app.route('/add', methods=["POST", "GET"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("submitted")
        newcafe = Cafe(name=form.name.data, 
                        map_url=form.map_url.data,
                        img_url=form.img_url.data,
                        location=form.location.data,
                        seats =form.seats.data,
                        has_toilet = form.has_toilet.data,
                        has_wifi = form.has_wifi.data,
                        has_sockets = form.has_sockets.data,
                        can_take_calls = form.can_take_calls.data,
                        coffee_price = form.coffee_price.data)
        db.session.add(newcafe)
        db.session.commit()
        return redirect(url_for("cafe_list"))
    return render_template("add_cafe.html",form=form)

########################################## Update Record
@app.route('/update/<int:id>', methods=["POST", "GET"])
def update_cafe(id):

    cafe = db.session.query(Cafe).get(id)
    if request.method == "POST":
        if cafe:
            cafe.name = request.form.get("Name")
            cafe.coffee_price = request.form.get("Price")
            cafe.map_url = request.form.get("Map")
            cafe.img_url = request.form.get("Image")
            cafe.seats = request.form.get("Seats")
            # cafe.has_toilet = request.form.get("Toilet")
            # cafe.has_wifi = request.form.get("Wifi")
            # cafe.has_sockets = request.form.get("Sockets")
            # cafe.can_take_calls = request.form.get("Calling")
            db.session.commit()
            return redirect(url_for("cafe_list"))
        else : 
            flash('Invalid Id')
    return render_template('update.html',  cafe=cafe)

########################################## Delete Record
@app.route("/delete/<int:cafe_id>")
def delete_cafe(cafe_id):
    cafe = db.session.query(Cafe).get(cafe_id)
    if cafe:
        db.session.delete(cafe)
        db.session.commit()
        return redirect(url_for("cafe_list"))
    else:
        return '<h1>something went wrong</h1>'





if __name__ == '__main__':
    app.run(debug=True)
