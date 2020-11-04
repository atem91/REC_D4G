import pandas as pd
from io import StringIO

#recupere les donnees dont nous allons avoir beosin
#data = 'Tableau.csv'
#f = open('Tableau.csv')

given_data_institut = pd.read_csv('Tableau_utf8.csv', error_bad_lines=False)
print(given_data_institut)
given_data_insee = pd.read_csv('departement_region.csv', error_bad_lines=False)
#print(given_data_insee)

#selection of department and region, add it on a new tab
#departement = given_data_insee.iloc[:,3]
#print(departement)
