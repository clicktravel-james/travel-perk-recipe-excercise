# travel-perk-recipe-excercise
The exercise described in the onboarding to showcase my new found knowledge of Django and its rest framework.

## Project Docker Commands

#### Build
```
docker-compose build
```
Builds the docker image with all the dependencies in the docker compose file.

#### Initialise Django project
```
docker-compose run --rm recipe_app sh -c "django-admin.py startproject app ."
```
This command created the Django app and initialised the based the content for the project.

#### Create new Django apps
```
docker-compose run --rm recipe_app sh -c "python manage.py startapp {name_of_app}"
```
This command will create a new app with the name given so you can extend Django.

#### Make and update the model 
```
docker-compose run --rm recipe_app sh -c "python manage.py makemigrations core"
```
As all the models are stored in the core app, this will generae the database migrations to support new models.

#### Manually run tests and linting 
```
docker-compose run --rm recipe_app sh -c "python manage.py test && flake8"
```
Any unit tests file and functions that have the prefix 'test_' will be run along with flake 8 linting.

#### Create super user for Django admin 
```
docker-compose run recipe_app sh -c "python manage.py createsuperuser"
```
Enables you to add a superuser that can control the Django admin pages.