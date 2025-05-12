from flask import Flask
from utils import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Caleb0804@localhost/trueke'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
app.register_blueprint(students)
