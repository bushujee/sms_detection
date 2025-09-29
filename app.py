from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Annotated
import pickle
import pandas as pd
from fastapi.responses import JSONResponse

# Load model and vectorizer
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('vectorizer.pkl', 'rb') as f:
    tkfd = pickle.load(f)

app = FastAPI()

class UserInput(BaseModel):
    message: Annotated[str, Field(..., description="Enter the message in the email")]

# Root endpoint (to test server works)
@app.get("/")
def home():
    return {"message": "API is running! Go to /docs to test predictions."}

# Prediction endpoint
@app.post("/predict")
def pred_out(data: UserInput):
    try:
        # Vectorize input text
        text_vec = tkfd.transform([data.message])

        # Model prediction (0 or 1)
        prediction = model.predict(text_vec)[0]

        # Map numeric label -> text label
        label_map = {0: "not spam", 1: "spam"}
        prediction_label = label_map.get(prediction, str(prediction))

        return JSONResponse(status_code=200, content={"prediction": prediction_label})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
