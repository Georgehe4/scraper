import pandas as pd

# end of 2010 = 1293800399
# there are leap years so year != standard increment
# don't need bound for 2017 because start with 2017 (entire file)

yearBounds = [1293839999, 1325375999, 1356998399, 1388534399, 1420070399, 1451606399, 1483228799, 1514764799]
startYear = 2010

# broad non-dev data
df = pd.read_csv('broad.csv')
df = df.sort_values(by=['timestamp'])
df = df.drop_duplicates(subset=['from_cluster_id', 'to_cluster_id'], keep='first')
for i in yearBounds:
    year = str(startYear + yearBounds.index(i))
    filename = 'broad' + year + '.csv'
    print filename
    df[df['timestamp'] < i].to_csv(filename, index=False)

# dev data
df2 = pd.read_csv('dev.csv')
df2 = df2.drop_duplicates()
df2 = df2.sort_values(by=['timestamp'])
df2 = df2.drop_duplicates(subset=['from_cluster_id', 'to_cluster_id'], keep='first')
for i in yearBounds:
    year = str(startYear + yearBounds.index(i))
    filename = 'dev' + year + '.csv'
    print filename
    df2[df2['timestamp'] < i].to_csv(filename, index=False)
