import os
import sys
from flask import Flask, request, abort, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actors, Movies
from auth import AuthError, requires_auth
from datetime import datetime


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response
    # ----------------------------------------------------------------------------#
    # Routes
    # ----------------------------------------------------------------------------#

    @app.route('/')
    def get_greeting():
        excited = os.environ['EXCITED']
        greeting = "Hello"
        if excited == 'true':
            greeting = greeting + "!!!!!"
        return  greeting

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def view_movies(payload):
        movies = Movies.query.all()
        if len(movies) == 0:
           return jsonify({'success': True, 'actors': [movie.format()
                       for movie in movies]}), 200
        else:
            abort(404)

 


    # ----------------------------------------------------------------------------#
    # error handlers
    # ----------------------------------------------------------------------------#


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)