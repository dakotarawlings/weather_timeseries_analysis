#%%

import requests
import pandas as pd
URL="http://127.0.0.1:5000/temperatureForecast"
headers={"Content-Type": "application/json"}
r=requests.get(URL, headers=headers,)


#print(r)
print(r.json()) 