from preprocessing import remove_org_descriptors
import pandas as pd 

data = pd.read_csv('env/data.csv')

data = data.apply(remove_org_descriptors)
