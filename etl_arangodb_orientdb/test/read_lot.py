import json

from pyArango.connection import *
import pandas as pd
from pyArango.query import SimpleQuery

conn = Connection(username="admin", password="admin")
db = conn["palamax_final"]
lot = db["Lot"]
# for v in lot.fetchAll():
#     print(v)
data = str(lot.fetchAll()).replace("'","\"")
print(type(data),data)
df = pd.read_json(data,orient='records')
print(df.to_string())
