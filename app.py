import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.sql.expression import true
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

    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(token):
        selection = Movies.query.all()

        movies = []

        for movie in selection:
            movies.append(movie.format())

        return jsonify({
            'status': True,
            'movies': movies
        })

    @app.route("/movies/add", methods=['POST'])
    @requires_auth('post:movies')
    def add_movie(token):        
            data = request.get_json()
            if 'title' in data:
                if data['title'] is None:
                    abort(400)
            if 'release_date' in data:
                if data['release_date'] is None:
                    abort(400)              
            new_movie = Movies(title= data['title'],
                            release_date = data['release_date'])                          
            new_movie.insert()
            return jsonify({
                    "success":True,
                    "movies":data}),200

        
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movie')
    def update_movies(payload, movie_id):
        body = request.get_json()
        movie = Movies.query.filter(Movies.id == movie_id).one_or_none()
        print(movie)
        if movie is None:
            abort(404)

        new_title = body.get('title', None)
        new_release_date = body.get('release_date', None)

        if new_title is not None:
            movie.title = new_title
        else:
            movie.title = movie.title

        if new_release_date is not None:
            movie.release_date = new_release_date
        else:
            movie.release_date = movie.release_date

        try:
            movie.update()
        except Exception:
            abort(422)
        return jsonify({
                "success": True,
                "Movie": movie.format()
            }), 200


    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movies(payload, movie_id):
        try:
            movie = Movies.query.filter(
                                    Movies.id == movie_id).one_or_none()
            if movie is None:
                abort(404)

            movie.delete()
            return jsonify({
                'success': True,
                'deleted': movie_id}), 200

        except Exception:
            print(sys.exc_info())
            abort(422)
    # ----------------------------------------------------------------------------#
    # error handlers
    # ----------------------------------------------------------------------------#

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
          "success": False,
          "error": 400,
          "message": "bad request"
          }), 400

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable."
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "The server can not find the requested resource."
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
            }), 405

    @app.errorhandler(AuthError)
    def auth_error(error):
        print(error)
        return jsonify({
            "success": False,
            "error": 400,
            "message": "unauthorized."
        }), 400
    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)