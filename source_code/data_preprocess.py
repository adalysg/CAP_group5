import pandas as pd

# Loading the dataset
df = pd.read_csv('cleaned_airbnb.csv')

# Drops all the objects with an empty 'price' attribute
df = df.dropna(subset=['price'])
# Drops all empty objects
df.dropna()

# Outlier Detection [Price] Using IQR

Q1 = df['price'].quantile(0.25)
Q3 = df['price'].quantile(0.75)
IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

df = df[(df['price'] >= lower) & (df['price'] <= upper)]

# Make a new CSV file with the converted currencies.
df.to_csv('cleaned_airbnb.csv', sep=',', encoding='utf-8', index=False, header=True)