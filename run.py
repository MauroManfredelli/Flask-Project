# run.py

import os

from app import create_app

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)


if __name__ == '__main__':
    app.run()

# We create the app by running the create_app function and passing in the configuration name. We get this from the OS
# environment variable FLASK_CONFIG. Because we are in development, we should set the environment variable to development.