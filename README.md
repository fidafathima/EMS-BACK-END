# Full-Stack Project: Django API + React Frontend
## This is the back-end developed using Django rest framework
 The following instructions will guide you through setting up and running back-end

# Basic Features
- Custom User model and authentication using email and password.
- JWT authentication.
- CRUD endpoints for recipe.
- Search functionality for recipes.
- Frontend is built using React.js and can be found here (https://github.com/fidafathima/EMS-BE.git)
# Prerequisites
- Python 3.8 or later
- pip (Python package installer)
- virtualenv

  # Steps
- Clone this repository to your local machine.
   - git clone (https://github.com/fidafathima/EMS-BACK-END.git)
- Create a python virtual environment and activate it.
  - python -m venv venv
  - source venv/bin/activate
  - On Windows, use `venv\Scripts\activate`

- Open up your terminal and run the following command to install the packages used in this project.
  - $ pip install -r requirements.txt
- Set up a Postgres database for the project.
- Create a .env file in the django-backend directory. Use .env.example as a template
- Run the following commands to setup the database tables and create a super user.
  - $ python manage.py migrate
  - $ python manage.py createsuperuser
- Run the development server using:
  - $ python manage.py runserver
- Open a browser and go to http://localhost:8000/.  
