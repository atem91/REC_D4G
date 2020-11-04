from flask_sqlalchemy import SQLAlchemy

from .views import app

db = SQLAlchemy(app)


class Zone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    CityName = db.Column(db.String(300), nullable=False)
    PostCode = db.Column(db.String(300), nullable=True)
    District = db.Column(db.String(300), nullable=True)

    def __init__(self, CityName, PostCode = None, District = None):
        self.CityName = CityName
        self.PostCode = PostCode
        self.District = District


db.create_all()