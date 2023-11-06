# Setting up the environment (noted it might change the version of your dependencies/ packages)

pip install -r requirements.txt

# To run the server

python manage.py runserver

# To access the website

## To access the weather page
http://127.0.0.1:8000/weather/

## To login and sign up
http://127.0.0.1:8000/login/
http://127.0.0.1:8000/logout/
http://127.0.0.1:8000/sign/

# GitHub repository link
https://github.com/Andrewxlokw/weatherApp#to-run-the-server

# Design changes

## Core feature

removed uv index from the core feature due to api not supporting it

removed future and previous weather forecast from the core feature due to the free version not supporting it

## Additional features
remove the ability for the user to send feedback related to accuracy due to this feature makes less sense in practice,
this feature has been replaced with activities recommendations after the proposal disscussion

removed sharing feature due to the app not having a proper way to communicate with other people, 
sharing the information with other social networks is possible, but it will make increase the scope of the project

## Minor changes

Removed email addresses from the signin feature due to the website not needing features that requires email addresses

