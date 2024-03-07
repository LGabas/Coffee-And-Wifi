from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, SelectField
from wtforms.validators import DataRequired, Length
import csv


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

"""---------- FORM CONFIG -----------------"""


class CafeForm(FlaskForm):
    cafe_name = StringField('Cafe Name', validators=[DataRequired(), Length(min=2)])
    cafe_location = URLField('Cafe Location on Google Maps(URL)', validators=[DataRequired()])
    opening_time = StringField('Opening Time', validators=[DataRequired()])
    close_time = StringField('Closing Time', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating', choices=['☕️', '☕️☕️', '☕️☕️☕️', '☕️☕️☕️☕️', '☕️☕️☕️☕️☕️'], validators=[DataRequired()])
    wifi_rating = SelectField('Wi-Fi Rating', choices=['✘', '💪', '💪💪', '💪💪💪', '💪💪💪💪', '💪💪💪💪💪'], validators=[DataRequired()])
    submit = SubmitField('Submit')


"""---------- FLASK ROUTES ----------------"""


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["POST", "GET"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():

        with open('cafe-data.csv', 'a', encoding='utf-8') as csv_file:
            csv_file.write(f"\n{form.cafe_name.data},"
                           f"{form.cafe_location.data},"
                           f"{form.opening_time.data},"
                           f"{form.close_time.data},"
                           f"{form.coffee_rating.data},"
                           f"{form.wifi_rating.data}")

        return redirect(url_for("cafes"))

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)

    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
