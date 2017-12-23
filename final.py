from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map, icons

import urllib.request
import json
from time import sleep

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


def getMarkers(actor):
    markers = []

    actor = actor.replace(" ", "%20")

    print(actor)

    # find actor id by name
    with urllib.request.urlopen(
                    "http://api.tmdb.org/3/search/person?api_key=6d8563e95c7e67ee7fb0c4a1ce93416e&query=" + actor) as url:
        data = json.loads(url.read().decode())

    if data["total_results"] == 0:
        return -1, markers, ""
    else:
        id = data["results"][0]["id"]
        print(id)
        name = data["results"][0]["name"]

    # get all movie of actor
    with urllib.request.urlopen("https://api.themoviedb.org/3/person/" + str(
            id) + "?api_key=6d8563e95c7e67ee7fb0c4a1ce93416e&append_to_response=credits") as url:
        data = json.loads(url.read().decode())

    # list of movies where actor played
    movies = data["credits"]["cast"]

    locations = {}

    i = 0;

    print("Number of movies: " + str(len(movies)))

    # go through all movies
    for movie in movies:
        # print(movie["title"])

        # get details of movie
        with urllib.request.urlopen("https://api.themoviedb.org/3/movie/" + str(
                movie["id"]) + "?api_key=6d8563e95c7e67ee7fb0c4a1ce93416e&language=en-US") as url:
            movie_detail = json.loads(url.read().decode())

        # go through countries where was this movie produced
        for country in movie_detail["production_countries"]:
            # print(country["name"])

            # if country is already in list of locations then add only name of this movie otherwise add this location
            if country["name"] in locations:
                locations[country["name"]].append(movie["title"])
            else:
                locations[country["name"]] = [movie["title"]]

        print("Movie number: " + str(i))
        i = i+1

    print(locations)

    print()

    # go through all countries
    for country in locations:
        marker = {}
        marker["icon"] = icons.dots.red
        marker["infobox"] = "<p><b>" + country + "</b></p>"


        print("Name of country: " + country + ":")

        country_req = country.replace(" ", "%20")

        with urllib.request.urlopen(
                                "https://maps.googleapis.com/maps/api/geocode/json?address=" + country_req + "&key=AIzaSyCxpj954vbyCaxIYIYFqOAx-qHfNM9Zo-g") as url:
            data = json.loads(url.read().decode())

        print("http://maps.googleapis.com/maps/api/geocode/json?address=" + country_req + "")
        print(data)

        if data["status"] == "OK":
            lat = data["results"][0]["geometry"]["location"]["lat"]
            lng = data["results"][0]["geometry"]["location"]["lng"]
            marker["lat"] = lat
            marker["lng"] = lng
            print("lat: " + str(lat))
            print("lng: " + str(lng))
        else:
            return -2, markers, ""

        print(locations[country])
        print()

        for i in locations[country]:
            marker["infobox"] += "<p>" + i + "</p>"


        markers.append(marker)

        sleep(0.5)

    print(markers)

    return 0, markers, name



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
            status, mymap.markers, getName = getMarkers(name)
            # mymap.markers = getMarkers(name)

            if(status == 0):
                flash('Map of countries, where were produced movies where ' + getName + ' played.')

            if (status == -1):
                flash('Error: Actor not found.')

            if (status == -2):
                flash('Error: Google API failed.')

        else:
            flash('Error: Input field is empty.')

    return render_template(
        'index.html',
        form=form,
        mymap=mymap
    )


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)