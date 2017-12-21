from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map, icons

app = Flask(__name__, template_folder="templates")

# you can set key as config
app.config['GOOGLEMAPS_KEY'] = "AIzaSyCxpj954vbyCaxIYIYFqOAx-qHfNM9Zo-g"

# you can also pass key here
GoogleMaps(app, key="AIzaSyCxpj954vbyCaxIYIYFqOAx-qHfNM9Zo-g")


# App config.
DEBUG = True
# app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


class ReusableForm(Form):
    name = StringField('Name:', validators=[validators.required()])


@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)

    mymap = Map(
        identifier="trdmap",
        varname="trdmap",
        lat=0,
        lng=0,
        zoom=1,
        style="height:500px;width:600px;margin:0;",
    )

    print
    form.errors
    if request.method == 'POST':
        name = request.form['name']
        print(name)

        if form.validate():
            # Save the comment here.
            flash('Name of actor: ' + name)

            mymap.markers=[
                    {
                        'icon': icons.dots.red,
                        'lat': 0,
                        'lng': 0,
                        'infobox': "Hello I am <b style='color:green;'>GREEN</b>!"
                    },
                    {
                        'icon': icons.dots.red,
                        'lat': 37.4300,
                        'lng': -122.1400,
                        'infobox': "Hello I am <b style='color:blue;'>BLUE</b>!"
                    },
                    {
                        'icon': icons.dots.red,
                        'lat': 37.4500,
                        'lng': -122.1350,
                        'infobox': (
                            "Hello I am <b style='color:#ffcc00;'>YELLOW</b>!"
                            "<h2>It is HTML title</h2>"
                            "<img src='//placehold.it/50'>"
                            "<br>Images allowed!"
                        )
                    }
                ]

        else:
            flash('Error: All the form fields are required. ')

    return render_template(
        'hello.html',
        form=form,
        mymap=mymap
    )


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)