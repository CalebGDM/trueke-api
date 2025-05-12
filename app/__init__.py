from app import app
from utils import db

with app.app_context():
    #db.create_all()
    pass


if __name__ == "__main__":
    app.run(debug=True)