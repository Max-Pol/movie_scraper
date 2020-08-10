import time
import json
import requests as r
from flask import Flask, jsonify
import errors  # Local package errors with custom exceptions

# Global variables (see README.md for explanations)
MOVIE_LIST = {"updated_at": 0, "data": []}

# Instantiate the app
app = Flask(__name__)
app.config.from_object('config')  # Load variables in config.py


# Main route: /movies
@app.route('/movies')
def movies():
    """Route which returns in a JSON format the list of the Studio Ghibli
    movies with the characters in them"""
    try:
        movies = list_movies()
    except errors.Unavailable as e:
        msg = "Failed to reach external API GHIBLI: " + str(e.__cause__)
        return jsonify({"error": msg}), 503
    # Note: Other exceptions could be caught here

    return jsonify(movies)


def list_movies(refresh_rate=app.config["REFRESH_RATE"]):
    """Returns a list of the Studio Ghibli movies with the characters in
    them. this list is either extracted from the cache if the data is still
    up to date, or fetched from the Ghibli API.

    Parameters
    ----------
    refresh_rate : int
        time in seconds from which the data must be updated with the Ghibli API
    """
    global MOVIE_LIST

    # If the movie list is not outdated, returns the value stored in cache
    if time.time() - MOVIE_LIST["updated_at"] < refresh_rate:
        return MOVIE_LIST["data"]
    # Otherwise, fetch the data from the external API Ghibli
    try:
        films = get_films()
        people = get_people()
    except (r.ConnectionError, r.Timeout) as e:
        raise errors.Unavailable from e  # Exception Chaining (python 3+)
    # Note: other errors could be caught here. For instance:
    # except r.HTTPError as e:
        # if e.response.status_code == 400:
        #     raise errors.NotFound from e

    # Build the movie list by matching films and people on field "url"
    film_index = {film["url"]: {**film, "people": []} for film in films}
    for p in people:
        for f in p["films"]:
            film_index[f]["people"].append(p["name"])
    # Note: It is of course possible to do this in a more optimized way if the
    # data becomes larger. For example, we could save memory by using indexes
    # instead of duplicating the film list, or improve overall efficiency
    # by using a JOIN statement from a database.

    # Update cache
    MOVIE_LIST["data"] = list(film_index.values())
    MOVIE_LIST["updated_at"] = time.time()

    return MOVIE_LIST["data"]


def get_films():
    """Fetch the Studio Ghibli films list from the Ghibli API"""
    resp = r.get(app.config['API_BASE_URL'] + "/films"
                 "?fields=title,url&limit=250")
    resp.raise_for_status()
    return resp.json()


def get_people():
    """Fetch the Studio Ghibli people list from the Ghibli API"""
    resp = r.get(app.config['API_BASE_URL'] + "/people"
                 "?fields=name,films&limit=250")
    resp.raise_for_status()
    return resp.json()


if __name__ == '__main__':
    # Run app
    app.run(debug=app.config['DEBUG'], host=app.config['HOST'],
            port=app.config['PORT'])
