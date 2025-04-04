from fastapi import FastAPI
from pydantic import BaseModel
from joblib import load
import pandas as pd
from datetime import datetime

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

async def get_temp(feature: FeatureType):
    try:
        country = feature.Country.capitalize()
        date = datetime.strptime(feature.Date, "%Y-%m-%d")

        encoded_country = encoder.transform([[country]])
        encoded_country_df = pd.DataFrame(encoded_country, columns=encoder.get_feature_names_out())

        if date >= start_date:
            days_diff = int(abs(start_date.to_pydatetime() - date).days)
        else:
            return {"Error": f"Date should be more than or equal to {start_date}"}

        new_country_input = pd.concat([encoded_country_df, pd.DataFrame({"days since": [days_diff]})], axis=1)
        
        predicted_temperature = model.predict(new_country_input)
        
        # Convert the NumPy array to a regular Python value that can be JSON serialized
        predicted_value = float(predicted_temperature[0]) if hasattr(predicted_temperature, "__len__") else float(predicted_temperature)
        
        return {"predicted_temperature": predicted_value}
    
    except Exception as e:
        return {"Error", e}

