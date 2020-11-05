import pandas as pd
from io import StringIO

#recupere les donnees dont nous allons avoir beosin
#data = 'Tableau.csv'
#f = open('Tableau.csv')

given_data_institut = pd.read_csv('Tableau_utf8.csv', error_bad_lines=False, delimiter=';')

new_table = pd.read_csv('departement_region.csv', error_bad_lines=False, delimiter=';', usecols=[1, 2, 5, 8])
print(given_data_institut)
#creation du tableau contenant les reg, dep, ville


