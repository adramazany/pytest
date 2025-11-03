import pandas as pd

data = {'timestamp': [1, 5, 3, 4, 2, 6, 8, 7], 'OC': ['C', 'O', 'C', 'C', 'O', 'O', 'C', 'O']}
df = pd.DataFrame(data=data)

df.sort_values("timestamp", inplace=True)

df.

print(df.to_string())


