
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
# ----------------------------------------------------------------------------#
    # Tests for success behavior of each endpoint
    # ----------------------------------------------------------------------------#

    # -----------------------------Movies API Test--------------------------------#
    # the user have enough permissions- casting assistant can view the movies
    def test_get_movies_success(self):
        response = self.client().get('/movies', headers= self.casting_assistant)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
if __name__ == "__main__":
    unittest.main()