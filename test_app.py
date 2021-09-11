
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
        self.database_name = 'caps'
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
if __name__ == "__main__":
    unittest.main()