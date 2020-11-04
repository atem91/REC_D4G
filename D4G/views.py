from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('D4G.config')
db = SQLAlchemy(app)


class Zone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    CityName = db.Column(db.String(300), nullable=False)

    def __init__(self, CityName):
        self.CityName = CityName



def init_db():
    db.drop_all()
    db.create_all()
    f = open('D4G/Tableau_utf8.csv')
    for line in f.readlines():
        splitted = line.split(';')
        if splitted[0]:
            db.session.add(Zone(splitted[0]))
    f.close()
    db.session.commit()

@app.route('/')
def index():
    res = ""
    for zone in Zone.query.all():
        res += zone.CityName + '<br/>'
    return res
