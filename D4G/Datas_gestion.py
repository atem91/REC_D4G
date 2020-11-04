import pandas as pd
from io import StringIO

#recupere les donnees dont nous allons avoir beosin
#data = 'Tableau.csv'
#f = open('Tableau.csv')

data = pd.read_csv('Tableau_utf8.csv', error_bad_lines=False)
print(data)


