import pandas as pd
from io import StringIO

#recupere les donnees dont nous allons avoir beosin
#data = 'Tableau.csv'
#f = open('Tableau.csv')

given_data_institut = pd.read_csv('Tableau_utf8.csv', error_bad_lines=False, delimiter=';')
#print(given_data_institut)
given_data_insee = pd.read_csv('departement_region.csv', error_bad_lines=False, delimiter=';')
#print(given_data_insee)

#selection of department and region, add it on a new tab
departement = given_data_insee.iloc[:,2]
#print(departement)
region = given_data_insee.iloc[:,1]
#print(region)

new = given_data_institut.sort_values(by='Code Iris')
print(new)
#given_data_insee['IRIS'] = given_data_insee['IRIS'].astype(int)
new_dep = given_data_insee.sort_values(by='IRIS', inplace=True)
print(new_dep)
