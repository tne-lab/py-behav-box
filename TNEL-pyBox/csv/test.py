import pandas
import random

random.seed()

df = pandas.read_csv('data.csv',index_col='trial')
for shock in length(df['shock']):
    df['shock',shock] = random.randint(0,1)
print(df)
