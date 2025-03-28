from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

class FeatureType(BaseModel):
    Country: str
    Date: str



@app.post("/")
async def get_temp(feature:FeatureType):
    pass