from flask import Flask
import os

app = Flask(__name__, static_folder=os.path.join(os.getcwd(), 'assets'))
logger = app.logger
