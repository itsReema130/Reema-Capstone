# Udacity Casting Agency Project
This project models a company that is responsible for creating movies and managing and assigning actors to those movies. The system simplify and streamline the process of Executive Producer within the company. It was done as capstone project for full stack nanodgree. this project test backend knowledge third party services intgration.


## Getting Started

### Installing Dependencies

To start the project locally, you need to have the following tools:
1. Python3 and PIP (Back-end)

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)



#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the root of the directory and run:

```bash
pip3 install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 


## Running the server locally in development environment

From within the `root` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
pip install -r requirements.txt
source setup.sh
python app.py
```

the `source setup.sh` will prepare all the needed environment variables to run the server.


## API Reference

### Introduction

The API builded to make users eable to perform CRUD operations on Casting Agency database easily. It have been builded using Flask micro-framework, which is Python framework.
This API was builded for the requirments of graduating of the FSND nanodegree of Udactiy.
All the responses of the API is in JSON format.

### Getting Started

#### Base URL

This project is deployed and available on Heroku:
```
https://reema-capstone.herokuapp.com
```

### Error

The API have clear and defined errors that will make the debug process easier for developers.

#### Error Types:

- 404 - Not Found
- 400 - Bad Request
- 422 - Unprocesaable
- 401 - Unauthorized

#### Error Response Example:

```
{
    "success": False,
    "error": 404,
    "message": "Resource Not Found"
}
```

### Endpoints Library

This section will contain all the endpoints with their response examples to make everything clear for the users of our API

#### GET /actors

- Return: return list of all the available actors.

- Sample Request: ```curl https://fsnd-nora-casting.herokuapp.com/actors```

- Arguments: None

- Sample Response:
    ```
    {
          "success": True,
          "actors": [
            {
              "id": 1,
              "name": "Nora Othman",
              "gender": "Female",
              "age": 20
            }, 
            {
              "id": 5,
              "name": "Marly Rose",
              "gender": "Female",
              "age": 500
            }
          ]
    }
    ```
#### GET /movies

- Return: return list of all the available movies.

- Sample Request: ```curl https://reema-capstone.herokuapp.com/movies```

- Arguments: None

- Sample Response:
    ```
{
    "movies": [
        {
            "id": 1,
            "release date": "Thu, 06 Oct 1988 00:00:00 GMT",
            "title": "Titanic"
        },
        {
            "id": 2,
            "release date": "Sat, 21 Nov 2020 00:00:00 GMT",
            "title": "Cyper Bunk"
        },
        {
            "id": 3,
            "release date": "Thu, 22 Nov 1934 00:00:00 GMT",
            "title": "IT HAPPENED ONE NIGHT"
        },
        {
            "id": 5,
            "release date": "Fri, 24 Jul 1936 00:00:00 GMT",
            "title": "MODERN TIMES"
        },
        {
            "id": 4,
            "release date": "Wed, 25 Sep 1940 00:00:00 GMT",
            "title": "REBECCA"
        }
    ],
    "status": true
}
    ```

#### DELETE /actors/id

- Return: 
    - the deleted actor ID and result of success state.

- Sample Request: ```curl -X "DELETE" https://fsnd-capstone-asiri.herokuapp.com/actors/2```

- Arguments: 
    - it take the id of the actor in the URL after the ```actors/```

- Sample Response:
    ```
    {
        "success": True,
        "actor_id": 2
    }
    ```

#### DELETE /movies/id

- Return: 
    - the deleted movie ID and result of success state.

- Sample Request: ```curl -X "DELETE" https://fsnd-capstone-asiri.herokuapp.com/movies/5```

- Arguments: 
    - it take the id of the movie in the URL after the ```movies/```

- Sample Response:
    ```
    {
        "success": True,
        "movie_id": 2
    }
    ```

#### POST /actors

- Return: 
    - the request success state.
    - the created actor object.
    - the ID of the created actor.

- Sample Request: 
    ```curl -d '{"name": "Omar Mohammed", "age": 30, "gender": "Male"}' -H "Content-Type: application/json" -H "Authorization: Bearer <TOKEN>" -X "POST" https://fsnd-capstone-asiri.herokuapp.com/actors```

- Arguments: 
    - None

- Required Headers:
    - the request need to include authorized and valid JWT token.
    - Content-Type: application/json

- Sample Response:
    ```
    {
        "success": True,
        "actor": {
            "id": 15,
            "name": "Omar Mohammed",
            "gender": "Male",
            "age": 30
        },
        "actor_id": 15
    }
    ```

#### POST /movies

- Return: 
    - the request success state.
    - the created movie object.
    - the ID of the created movie.

- Sample Request: 
    ```curl -d '{"title": "Rick and morty"}' -H "Content-Type: application/json" -H "Authorization: Bearer <TOKEN>" -X "POST" https://reema-capstone.herokuapp.com/movies/add```

- Arguments: 
    - None

- Required Headers:
    - the request need to include authorized and valid JWT token.
    - Content-Type: application/json

- Sample Response:
    ```
    {
    "movies": {
        "release_date": "2 Sep,2013",
        "title": "rick and morty"
    },
    "success": true
}
    ```

#### PATCH /actors

- Return:
    - the request success state.
    - the modified actor object.
    - the ID of the modified actor.

- Sample Request: 
    ```curl -d '{"name": "omar mohammed", "age": 28, "gender": "male"}' -H "Content-Type: application/json" -H "Authorization: Bearer <TOKEN>" -X "PATCH" https://fsnd-capstone-asiri.herokuapp.com/actors/15```

- Arguments: 
    - the ID of the actor that need to modified.

- Required Headers:
    - the request need to include authorized and valid JWT token.
    - Content-Type: application/json

- Sample Response:
    ```
    {
        "success": True,
        "actor": {
            "id": 15,
            "name": "omar mohammed",
            "gender": "male",
            "age": 28
        },
        "actor_id": 15
    }
    ```

#### PATCH /movies

- Return:
    - the request success state.
    - the modified movie object.
    - the ID of the modified movie.

- Sample Request: 
    ```curl -d '{"title": "lockdown"}' -H "Content-Type: application/json" -H "Authorization: Bearer <TOKEN>" -X "PATCH" https://fsnd-capstone-asiri.herokuapp.com/movies/87```

- Arguments: 
    - the ID of the movie that need to modified.

- Required Headers:
    - the request need to include authorized and valid JWT token.
    - Content-Type: application/json

- Sample Response:
    ```
    {
        "success": True,
        "movie": {
            "id": 87,
            "title": "lockdown",
            "release": "7 Oct, 2020"
        },
        "movie_id": 87
    }
    ```

## Authentication and Permissions

Authentication is handled via [Auth0](https://auth0.com).

All endpoints require authentication, and proper permission. 

For testing, you can use the Tokens that available in the .env file.

API endpoints use these roles and permissions:

- Casting Assistant:
    * 'get:actor' (remove actor from the casting agency database).
    * 'get:movie' (edit or modify actor data that exist in the casting agency database).

- Casting Director:
    * Same as the Casting Assistant permissions, plus
    * 'delete:actor' (remove actor from the casting agency database).
    * 'patch:actor' (edit or modify actor data that exist in the casting agency database).
    * 'patch:movie' (edit or modify actor data that exist in the casting agency database).
    * 'post:actors' (create new actors in the casting agency database).

- Executive Director:
    * Same as the Casting Director permissions, plus
    * 'delete:movie' (remove movie from the casting agency database).
    * 'post:movies' (create new movies in the casting agency database).