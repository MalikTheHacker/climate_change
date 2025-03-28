from fastapi import FastAPI
from pydantic import BaseModel
from joblib import load
import pandas as pd
import json

start_date = load("start_date.gz")
encoder = load("encoder.gz")
model = load("temp_model.gz")

app = FastAPI()

class FeatureType(BaseModel):
    Country: str
    Date: str


@app.get("/")
async def test():
    return "Hola to the web"

@app.post("/")
async def get_temp(feature:FeatureType):
    
    country = feature.Country.capitalize()
    date = pd.to_datetime(feature.Date)

    encoded_country = encoder.transform([[country]])
    encoded_country_df = pd.DataFrame(encoded_country, columns=encoder.get_feature_names_out())

    if date >= start_date:
        days_diff = int(abs(start_date - date).days)
    else:
        return {"Error": f"Date should be more than or equal to {start_date}"}

    new_country_input =  pd.concat([encoded_country_df, pd.DataFrame({"days since": [days_diff]})], axis=1)
    
    predicted_temperature = model.predict(new_country_input)
    print("Hello")
    return predicted_temperature


