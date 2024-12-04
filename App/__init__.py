from flask import Flask
from App.config import Config
from App.service_downloader import downloader


# Create a flask object with the same name as this module (APP)
app = Flask(__name__)
app.config.from_object(Config)  # load the configuration from the config.py file

from App import routes
