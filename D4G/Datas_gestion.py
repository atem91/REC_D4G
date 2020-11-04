import pandas as pd
from io import StringIO

#recupere les donnees dont nous allons avoir beosin
#data = 'Tableau.csv'
data = pd.read_csv('Tableau.csv')
print(data)


