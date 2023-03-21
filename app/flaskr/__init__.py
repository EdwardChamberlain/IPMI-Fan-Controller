from flask import Flask, request
from flask_bootstrap import Bootstrap


from config import Flask_Config


app = Flask(__name__)
app.config.from_object(Flask_Config)
bootstrap = Bootstrap(app)


from flaskr import routes
