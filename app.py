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

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movies(payload):
        body = request.get_json()
        add_id = body.get('id', None)
        add_title = body.get('title', None)
        add_release_date = body.get('release_date', None)
     

        if not (add_id and add_title and add_release_date):
            abort(
                400, {
                    'message': 'Please, Fill all the required fields'})

        try:
            # insert the new Q to the database
            movie = Movies(mId=add_id,
                                title=add_title,
                                release_date=add_release_date)
            movie.insert()
            return jsonify(
                {'success': True,
                'created': movie.id})
        except BaseException:
            # If anything went wrong, handle the 422 error
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