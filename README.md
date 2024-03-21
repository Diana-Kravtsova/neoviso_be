# neoviso-be

Neoviso test task back-end


## Getting Started

local build

1. Install Python 3 and pip
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate`
4. Install Django: `pip install django`
5. Create a Django project: `django-admin startproject myproject`
6. Navigate to the project folder: `cd myproject`
7. Install dependencies: `pip install -r requirements.txt`
8. Create a database: `python manage.py migrate`
9. Start the development server: `python manage.py runserver`

## Commands

* `python manage.py migrate`: Apply migrations
* `python manage.py createsuperuser`: Create a superuser
* `python manage.py runserver`: Start the development server

Runs the app in the development mode.\
Open [http://127.0.0.1:8000](http://127.0.0.1:8000) to view it in your browser.

## Links to connected repos

* [Frontend GitHub repo](https://github.com/Diana-Kravtsova/neoviso-fe)
* [Deploy GitHub repo](https://github.com/Diana-Kravtsova/neoviso-deploy)

### Deployment

build image:
`docker build -t neoviso-be:latest .`

configure environment and run container.
