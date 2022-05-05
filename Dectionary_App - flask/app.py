from datetime import date
from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route("/",  methods=['GET', 'POST'])
def owl_dictionary():
    year = date.today().year
    print(year)
    if request.method == 'POST':
        word = request.form['searchWord']
      
        try:           
            url = f"https://owlbot.info/api/v4/dictionary/{word}"
            header = {'Authorization': 'Token ' +
                      '595782793874b220229f85a841578fdb1de7021a'}

            response = requests.get(url, headers=header)
            data = response.json()
           
            return render_template('index.html', data=data, word=word, footer_year= year)

        except:
            return render_template('index.html',footer_year= year)

    return render_template('index.html', footer_year= year)


if __name__ == "__main__":
    app.run(debug=True)
