from flask import Flask, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__)

app.config.from_object('D4G.config')
db = SQLAlchemy(app)


class Indice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    CityName = db.Column(db.String(300), nullable=False)
    AccessInfo = db.Column(db.Integer(), nullable=False)
    AccessInterface = db.Column(db.Integer(), nullable=False)
    AdminCompetences = db.Column(db.Integer(), nullable=False)
    GlobalScore = db.Column(db.Integer(), nullable=False)
    NumCompetences = db.Column(db.Integer(), nullable=False)
    def __init__(self, CityName, AccessInfo, AccessInterface, AdminCompetences, GlobalScore, NumCompetences):
        self.CityName = CityName
        self.AccessInfo = AccessInfo
        self.AccessInterface = AccessInterface
        self.AdminCompetences = AdminCompetences
        self.GlobalScore = GlobalScore
        self.NumCompetences = NumCompetences

class Zone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    CityName = db.Column(db.String(300), nullable=False)
    CityIrisName = db.Column(db.String(300), nullable=False)
    DepartmentNumber = db.Column(db.String(10), nullable=False)
    RegionNumber = db.Column(db.String(10), nullable=False)


    def __init__(self, CityName, CityIrisName, DepartmentNumber, RegionNumber):
        self.CityName = CityName
        self.CityIrisName = CityIrisName
        self.DepartmentNumber = DepartmentNumber
        self.RegionNumber = RegionNumber


def init_db():
    db.drop_all()
    db.create_all()
    given_data_institut = pd.read_csv('D4G/Tableau_utf8.csv', error_bad_lines=False, delimiter=';')
    new_table = pd.read_csv('D4G/departement_region.csv', error_bad_lines=False, delimiter=';', usecols=[1, 2, 5, 8])
    f = open('D4G/Tableau_utf8.csv')
    for index, line in new_table.iterrows():
        db.session.add(Zone(line['LIBCOM'], line['LIBIRIS'], line['DEP'], line['REG']))
    for index, line in given_data_institut.iterrows():
        db.session.add(Indice(line['Nom Iris'], line["ACCES A L'INFORMATION"], line["ACCÈS AUX INTERFACES NUMERIQUES"], line["COMPETENCES ADMINISTATIVES"], line["SCORE GLOBAL "], line["COMPÉTENCES NUMÉRIQUES / SCOLAIRES"]))
    f.close()
    db.session.commit()


@app.route('/')
def index():
    res = ""
    citys = []
    for zone in db.session.query(Indice.CityName.distinct().label("CityName")):
        citys.append(zone.CityName)
    return render_template('template_IRN.html', citys=citys, len=len(citys), url_for=url_for)


@app.route('/search')
def search():
    city = request.args.get('city')
    zone = Indice.query.filter_by(CityName=city).first()
    return render_template('result.html', AccessInfo=zone.AccessInfo, AdminCompetences=zone.AdminCompetences, NumCompetences=zone.NumCompetences, AccessInterface=zone.AccessInterface)