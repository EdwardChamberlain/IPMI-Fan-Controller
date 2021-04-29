from flask import Flask

from config import Flask_Config


app = Flask(__name__)
app.config.from_object(Flask_Config)


from flaskr import routes