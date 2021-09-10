
import os
import sys
from flask import Flask, request, abort, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import *
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
    @app.route('/')
    def get_greeting():
        excited = os.environ['EXCITED']
        greeting = "Hello"
        if excited == 'true':
            greeting = greeting + "!!!!!"
        return  greeting

    # *********************************************
    #           Movies                            #
    # *********************************************

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def view_movies(payload):
        movies = Movies.query.all()
        if len(movies) == 0:
            abort(404)
        return jsonify({'success': True, 'actors': [movie.format()
                       for movie in movies]}), 200

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movies(payload):
        try:
            request_data = request.get_json()
            release = datetime.utcnow()
            if 'title' not in request_data:
                abort(400)

            if 'release_date' in request_data:
                release = request_data['release_date']

            movie = Movies(title=request_data['title'], release=release)
            movie.insert()

            return jsonify({'success': True, 'movie': movie.format(),
                        'movie_id': movie.id})

        except Exception:
            print(sys.exc_info())
            abort(500)
                      
    return app

app = create_app()

if __name__ == '__main__':
    app.run()