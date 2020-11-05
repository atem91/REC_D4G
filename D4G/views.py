from flask import Flask, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__)

app.config.from_object('D4G.config')
db = SQLAlchemy(app)


class Indice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    CityName = db.Column(db.String(300), nullable=True)
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
"""
class Zone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    CityName = db.Column(db.String(300), nullable=False)
    CityIrisName = db.Column(db.String(300), nullable=False)
    DepartmentNumber = db.Column(db.String(10), nullable=False)
    RegionNumber = db.Column(db.String(10), nullable=False)
    CodeCom = db.Column(db.String(10), nullable=False)


    def __init__(self, CityName, CityIrisName, DepartmentNumber, RegionNumber, CodeCom):
        self.CityName = CityName
        self.CityIrisName = CityIrisName
        self.DepartmentNumber = DepartmentNumber
        self.RegionNumber = RegionNumber
        self.CodeCom = CodeCom
"""

class ville(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    CityName = db.Column(db.String(300), nullable=False)
    department_code = db.Column(db.String(10), nullable=False)
    zip_code = db.Column(db.String(10), nullable=True)

    def __init__(self, CityName, department_code, zip_code):
        self.CityName = CityName
        self.department_code = department_code
        self.zip_code = zip_code

class department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(100), nullable=False)
    department_code = db.Column(db.String(10), nullable=False)
    region_code = db.Column(db.String(10), nullable=False)

    def __init__(self, department_name, department_code, region_code):
        self.department_name = department_name
        self.department_code = department_code
        self.region_code = region_code

class region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    region_name = db.Column(db.String(100), nullable=False)
    region_code = db.Column(db.String(10), nullable=False)

    def __init__(self, region_name, region_code):
        self.region_name = region_name
        self.region_code = region_code

def init_db():
    db.drop_all()
    db.create_all()
    given_data_institut = pd.read_csv('D4G/Tableau_utf8.csv', error_bad_lines=False, delimiter=';')
    new_table = pd.read_csv('D4G/departement_region.csv', error_bad_lines=False, delimiter=';', usecols=[1, 2, 4, 5, 8], dtype={'COM' : str, 'DEP' : str})
    departments = pd.read_csv('D4G/departments.csv', error_bad_lines=False, delimiter=',', usecols=[1,2,3], dtype={'region_code' : str, 'code': str, 'name': str})
    regions = pd.read_csv('D4G/regions.csv', error_bad_lines=False, delimiter=',', usecols=[1,2], dtype={'code' : str, 'name': str})
    cities = pd.read_csv('D4G/cities.csv', error_bad_lines=False, delimiter=',', usecols=[1,2,3,4], dtype={'department_code':str, 'insee_code': str, 'zip_code':str, 'name' :str})
    #for index, line in new_table.iterrows():
    #    db.session.add(Zone(line['LIBCOM'], line['LIBIRIS'], line['DEP'], line['REG'], line['COM']))
    for index, line in given_data_institut.iterrows():
        db.session.add(Indice(line['Nom Com'], line["ACCES A L'INFORMATION"], line["ACCÈS AUX INTERFACES NUMERIQUES"], line["COMPETENCES ADMINISTATIVES"], line["SCORE GLOBAL "], line["COMPÉTENCES NUMÉRIQUES / SCOLAIRES"]))
    for _, line in cities.iterrows():
        db.session.add(ville(line['name'], line['department_code'], line['zip_code']))
    for _, line in departments.iterrows():
        db.session.add(department(line['name'], line['code'], line['region_code']))
    for _, line in regions.iterrows():
        db.session.add(region(line['name'], line['code']))

    db.session.commit()


@app.route('/')
def index():
    #init_db()
    res = ""
    citys = []

    regions = region.query.all()
    for zone in db.session.query(Indice.CityName.distinct().label("CityName")).order_by(Indice.CityName):
        citys.append(zone.CityName)
    return render_template('template_IRN.html', citys=citys, len=len(citys), url_for=url_for,regions=regions)


@app.route('/search')
def search():
    city = request.args.get('city')
    zone = Indice.query.filter(Indice.CityName==city).all()
    return render_template('result.html', results=zone)

@app.route('/searchcp')
def searchcp():
    cp = str(request.args.get('code'))
    zone = db.session.query(Indice).join(ville, ville.CityName==Indice.CityName).filter(ville.zip_code == cp).all()
    #city = db.session.query(ville).filter(ville.zip_code == cp)
    #zone = Indice.query.filter(Indice.CityName==city).all()
    print(len(zone))
    return render_template('result.html', results=zone)

@app.route('/filter_department')
def filter_department():
    code = str(request.args.get('code'))
    departments = department.query.filter(department.region_code == code).all()
    return render_template('filter_departments.html', departments=departments)

@app.route('/filter_cities')
def filter_cities():
    code = str(request.args.get('code'))
    cities = ville.query.filter(ville.department_code == code).all()
    return render_template('filter_cities.html', cities=cities)