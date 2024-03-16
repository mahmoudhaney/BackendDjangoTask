# Backend Django Task

## Requirements
- [x] Create a `Django` Rest API called `blog` and integrate it into a new Django project.
- [x] Define a user model called "User" That extends `Django` AbstractUser Model and use this custom user model as your AUTH_USER_MODEL.
- [x] Use Token Authentication system for you authenticated your API.
- [x] Define a model called `Post` with the following fields
  - [x] Title (CharField)
  - [x] Content (TextField)
  - [x] Author (ForeignKey to User Model)
  - [x] Created at (DateTimeField, auto-populated with the current timestamp)
  - [x] Updated at (DateTimeField, auto-populated with the update timestamp)
- [x] Create appropriate views to perform the following tasks
  - [x] Register, Login, and logout for user.
  - [x] Publish post by specific user as Author.
  - [x] List Published posts with data about Author.
  - [x] Update and Delete Published posts by Author only.
- [x] Implement serializers to convert the `User` and `Post` model instances into `JSON` format and vice versa.
- [x] Write unit tests to ensure the correct functioning of the views and models.


## Extra
- [x] User logic is in a separate app called `accounts`.
- [x] Change Password endpoint.
- [x] Reset Password endpoint.
- [x] Unit Tests for all endpoints.


## Technologies
- `Django 4.2.6`
- `Django Rest Framework 3.14.0`
- `Pillow 10.0.1`
- `python-decouple 3.8`
- `django-rest-passwordreset 1.3.0`
- DB `sqlite`


## Setup

- Clone the repository using the command below:
```bash
git clone https://github.com/mahmoudhaney/BackendDjangoTask.git

```

- Navigate where the application is installed 

- Create a virtual environment:
```bash
# Let's install virtualenv first
pip install virtualenv

# Then we create our virtual environment
virtualenv env_name

```

- Activate the virtual environment:
```bash
env_name\scripts\activate

```

- Install the requirements:
```bash
pip install -r requirements.txt

```

- Create a `.env` file for important:
```bash
SECRET_KEY = 'your-key'
DEBUG = True
EMAIL_HOST_PASSWORD='your-google-app-key'

```

- Create a superuser 
```bash
python manage.py createsuperuser

```

- To run the App, we use:
```bash
python manage.py runserver

```


> ⚠ Then, the development server will be started at http://127.0.0.1:8000/

#

## How To Use
After running the server you can use [Postman](https://www.postman.com/downloads/) to try the APIs
1. Open Postman
2. Import the [APIs File](BackendDjangoTask.postman_collection.json) into your Postman workspace
3. Use APIs to add some Users and Posts for testing.

> ⚠ You can choose whatever you want to run the System APIs
