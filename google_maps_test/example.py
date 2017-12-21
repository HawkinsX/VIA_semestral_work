# coding: utf-8

from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map, icons

app = Flask(__name__, template_folder="templates")

# you can set key as config
app.config['GOOGLEMAPS_KEY'] = "AIzaSyCxpj954vbyCaxIYIYFqOAx-qHfNM9Zo-g"

# you can also pass key here
GoogleMaps(app, key="AIzaSyCxpj954vbyCaxIYIYFqOAx-qHfNM9Zo-g")


@app.route("/")
def mapview():

    mymap = Map(
        identifier="trdmap",
        varname="trdmap",
        lat=0,
        lng=0,
        zoom=1,
        style="height:500px;width:600px;margin:0;",
        markers=[
            {
                'icon': icons.dots.red,
                'lat': 1,
                'lng': -122.1419,
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
    )


    return render_template(
        'example.html',
        mymap=mymap
    )


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
