import pandas
import random

random.seed()

df = pandas.read_csv('data.csv',index_col='trial')
for i in range(1,len(df['shock'])-1):
    df['shock'][i] = random.randint(0,1)
    
print(df)
