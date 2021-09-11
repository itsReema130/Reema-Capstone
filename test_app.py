
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import create_app
from models import setup_db, Movies, Actors


class AgencyTestCase(unittest.TestCase):
    """This class represents the Agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""

        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'cab'
        self.database_path = "postgresql://{}:{}@{}/{}".format('reemaalhammadi',
                                                      'postgres',
                                                      'localhost:5432',
                                                      self.database_name)

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.drop_all()
            self.db.create_all()

        # ----------------------------------------------------------------------------#
        # Adding dummy data to the database 
        # ----------------------------------------------------------------------------#

        self.new_actor = {'name': 'Reema sultan', 'age': 21,
                          'gender': 'Female'}
        self.new_movie = {'title': 'Nora Dairy',
                          'release_date': datetime.utcnow()}
        for i in range(5):
            actor = Actors(name=self.new_actor['name'],
                          age=self.new_actor['age'],
                          gender=self.new_actor['gender'])
            actor.insert()
        for i in range(5):
            movie = Movies(title=self.new_movie['title'],
                          release_date=self.new_movie['release_date'])
            movie.insert()
        # ----------------------------------------------------------------------------#
        # Authorization token to start testing 
        # ----------------------------------------------------------------------------#

        self.casting_assistant = {
            "Authorization": "Bearer {}".format(os.environ.get('CASTING_ASSISTANT_TOKEN'))
        }
        self.casting_director = {
            "Authorization": "Bearer {}".format(os.environ.get('CASTING_DIRECTOR_TOKEN'))
        }
        self.executive_producer = {
            "Authorization": "Bearer {}".format(os.environ.get('EXECUTIVE_PRODUCER_TOKEN'))
        }
    def tearDown(self):
        """Executed after reach test"""

        pass
 # -----------------------------Movies API Test--------------------------------#
    # the user have enough permissions- casting assistant can view the movies
    def test_get_movies_success(self):
        response = self.client().get('/movies', headers= self.casting_assistant)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    
    # the user have enough permissions- excecutive producer can create movies
    def test_post_movie_success(self):
        response = self.client().post(
                                      '/movies',
                                      headers=self.executive_producer,
                                      json=self.new_movie)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    
    # the user have enough permissions
    def test_delete_movie_success(self):
        movie = Movies.query.all()[0]
        response = self.client().delete('/movies/{}'.format(movie.id),
                                        headers=self.executive_producer)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    # the user have enough permissions
    def test_patch_movies_success(self):
        movie = Movies.query.all()[0]
        response = self.client().patch('/movies/{}'.format(movie.id),
                                       headers=self.executive_producer,
                                       json=self.new_movie)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    
    # -----------------------------Actors API Test--------------------------------#

    # the user have enough permissions
    def test_get_actors_success(self):
        response = self.client().get('/actors', headers= self.casting_assistant)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    # the user have enough permissions
    def test_post_actor_success(self):
        response = self.client().post('/actors',
                                      headers=self.executive_producer,
                                      json=self.new_actor)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    
    # the user have enough permissions
    def test_delete_actor_success(self):
        actor = Actors.query.all()[0]
        response = self.client().delete('/actors/{}'.format(actor.id),
                                        headers=self.executive_producer)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    # the user have enough permissions
    def test_patch_actor_success(self):
        actor = Actors.query.all()[0]
        response = self.client().patch('/actors/{}'.format(actor.id),
                                       headers=self.executive_producer,
                                       json=self.new_actor)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    # ----------------------------------------------------------------------------#
    # Tests for error behavior of each endpoint
    # ----------------------------------------------------------------------------#

    # -----------------------------Movies API Test--------------------------------#
    # the user does not have permissions
    def test_post_movie_failure(self):
        response = self.client().post(
                                    '/movies',
                                    headers=self.casting_director,
                                    json=self.new_movie)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)

    # the user does not have permissions   
    def test_delete_movie_failure(self):
        movie = Movies.query.all()[0]
        response = self.client().delete('/movies/{}'.format(movie.id),
                                        headers=self.casting_director)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
    
    # no TOKEN provided 
    def test_patch_movies_failure(self):
        movie = Movies.query.all()[0]
        response = self.client().patch('/movies/{}'.format(movie.id),
                                       json=self.new_movie)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
    
    # -----------------------------Actors API Test--------------------------------#

    # no TOKEN provided
    def test_post_actor_failure(self):
        response = self.client().post('/actors', json=self.new_actor)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)

    # no TOKEN provided
    def test_delete_actor_failure(self):
        actor = Actors.query.all()[0]
        response = self.client().delete('/actors/{}'.format(actor.id))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)

    # no TOKEN provided
    def test_patch_actor_failure(self):
        actor = Actors.query.all()[0]
        response = self.client().patch('/actors/{}'.format(actor.id),
                                       json=self.new_actor)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
