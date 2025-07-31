from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, InputRequired, URL
import csv


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe Location on GMaps (URL)', validators=[DataRequired(),URL()])
    open_time = StringField('Opening time e.g. 8AM',validators=[DataRequired()])
    close_time = StringField('Closing time e.g. 5:30PM',validators=[DataRequired()])
    coffee = SelectField('Coffee rating',validators=[DataRequired()],choices=[
                                    ('☕', '☕ (Awful)'),
                                    ('☕☕', '☕☕ (Bad)'),
                                    ('☕☕☕', '☕☕☕ (Okay)'),
                                    ('☕☕☕☕', '☕☕☕☕ (Good)'),
                                    ('☕☕☕☕☕', '☕☕☕☕☕ (Excellent)')
                                                                                ])
    wifi = SelectField('Wifi Strength Rating', validators=[DataRequired()],
                              choices=[
                                  ('✘', '✘ (No Wifi)'),
                                  ('💪', '💪 (Poor)'),
                                  ('💪💪', '💪💪 (Okay)'),
                                  ('💪💪💪', '💪💪💪 (Good)'),
                                  ('💪💪💪💪', '💪💪💪💪 (Excellent)')
                              ])
    power = SelectField('Power Socket Availability', validators=[DataRequired()],
                               choices=[
                                   ('✘', '✘ (No Sockets)'),
                                   ('🔌', '🔌 (Few)'),
                                   ('🔌🔌', '🔌🔌 (Some)'),
                                   ('🔌🔌🔌', '🔌🔌🔌 (Many)')
                               ])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add',methods=["GET","POST"])
def add_cafe():
    form = CafeForm()
    if request.method=='POST' and form.validate_on_submit():
        list=[form.cafe.data,form.location.data,form.open_time.data,form.close_time.data,form.coffee.data,form.wifi.data,form.power.data]
        with open('cafe-data.csv','a',newline='',encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(list)
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        header=list_of_rows[0]
        data=list_of_rows[1:]
    return render_template('cafes.html', header=header, data=data)


if __name__ == '__main__':
    app.run(debug=True)
