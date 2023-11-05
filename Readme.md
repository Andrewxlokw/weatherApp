# Setting up the environment, note it might change the version of your dependencies/ packages

pip install -r requirements.txt

# To run the server

python manage.py runserver

# design changes,

## core feature

removed uv index from the core feature due to api not supporting it


removed previous weather forecast from the core feature due to the free version not supporting it

## additional features
remove the ability for the user to send feedback related to accuracy due to this feature makes less sense in practice,
this feature has been replaced with activities recommendations after the proposal disscussion


removed futures index from the core feature
The app shall allow users to share the weather information with other people 
