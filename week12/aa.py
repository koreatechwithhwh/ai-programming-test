import pandas as pd
df = pd.read_csv("scores_2026.csv")
print(df.head(5))
print(df['점수'].mean())