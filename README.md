# REU Project Recommendation Backend

This project was created as the backend for a mobile app developed for the University of Louisville's Knowledge Discovery and Web Mining Lab. The boilerplate code was taken from a starter Django template meant to be deployed onto Heroku, and the following few sections will be taken from that README. Skip to *REU Project* for information specific to the project.

## Features- taken from the boilerplate README

- Production-ready configuration for Static Files, Database Settings, Gunicorn, etc.
- Enhancements to Django's static file serving functionality via WhiteNoise.
- Latest Python 3.6 runtime environment.

## Deployment to Heroku- also from boilerplate README, but *important*

    $ git init
    $ git add -A
    $ git commit -m "Initial commit"

    $ heroku create
    $ git push heroku master

    $ heroku run python manage.py migrate

See also, a [ready-made application](https://github.com/heroku/python-getting-started), ready to deploy.

Note to lab: the steps shown above should be pursued only to deploy the application for the first time on a Heroku account

## Using Python 2.7?

Just update `runtime.txt` to `python-2.7.13` (no trailing spaces or newlines!).


## License: MIT

## Further Reading

- [Gunicorn](https://warehouse.python.org/project/gunicorn/)
- [WhiteNoise](https://warehouse.python.org/project/whitenoise/)
- [dj-database-url](https://warehouse.python.org/project/dj-database-url/)


# REU Project

The project, as an API meant to serve JSON and not webpages, utilizes [the Django REST framework](http://www.django-rest-framework.org/), and most of the Django code can be explained with tutorial resources from that site.

## Running the app

To setup the database (SQLite for development server), use the following commands:

    $ python manage.py makemigrations
    $ python manage.py migrate

This will setup the database migrations (needs to be run if changes are made to models) and apply them.

## Project structure

The *bias_reduction_server/* directory is present mostly for setup purposes (the Django REST framework wraps their application around that folder). For the purposes of extending the code, 99% of work will be done in *app/*

* **models.py** Defines database models. If this is changed, must run
* **serializers.py** Takes data from database and serialize into JSON or vice-versa
* **urls.py** Routes for the web application (i.e. where the API can point to)
* **views.py** Responsible for rendering responses pointed to in URLs (most routes endpoints automatically generated with Django REST framework)
* **prediction.py** handles all the recommendation logic (i.e. all the data science lives here). In the future, as the logic becomes more and more byzantine, should extend this into a folder with each subclassed method in its own file (or pull in a 3rd party lib).

## Prediction methods

The end-goal for the project is to make predictions using item-based filtering, collaborative filtering, matrix factorization methods, and compare the results with a novel method.
