import pandas as pd

# Load original Kaggle dataset
df = pd.read_csv('athlete_events.csv')

# Keep only useful columns
df = df[['Name','Sex','Age','Team','NOC','Games',
         'Year','Season','City','Sport','Event','Medal']]

# Keep recent Olympics only
df = df[df['Year'] >= 2000]

# Save reduced dataset
df.to_csv('athlete_events_small.csv', index=False)

print("Reduced CSV created successfully")