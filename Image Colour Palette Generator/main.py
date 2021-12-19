from flask import Flask, render_template, url_for, request, redirect
from werkzeug.utils import secure_filename
from colorthief import ColorThief
from datetime import datetime
import os


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "static/images/"

# CREATE  DYNAMIC FOOTER DATE
@app.context_processor
def inject_now():
    return {'footer_year': datetime.now().year}


@app.route('/', )
def home():
    return render_template("index.html")

@app.route("/result", methods=["POST", "GET"])
def result():
    file = request.files['file']
    print(file.filename)
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    full_image_path = f"static/images/{file.filename}"
    color_thief = ColorThief(full_image_path)
    top_colors = color_thief.get_palette(color_count=11)
    return render_template("colors.html", image=full_image_path, top_colors=top_colors)
    
if __name__ == '__main__':
    app.run(debug=True)


