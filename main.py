from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
from new_chat import generate_llm_recommendations, chat_with_bot  # ✅ Chatbot integration

# Load model
model = joblib.load("webpage chatbot/final_year_project_model.pkl")

# FastAPI app config
app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input schema
class LifeExpectancyInput(BaseModel):
    age: int
    country: str
    gender: str
    exercise: float
    diet: str
    medical: str
    stress: str
    smoking: str
    alcohol: str
    social: str
    bmi: float
    sleep: float
    heartRate: float
    spo2: float
    temperature: float

@app.post("/predict")
async def predict(data: LifeExpectancyInput):
    # Prepare input for model (exclude 'age')
    input_df = pd.DataFrame({
        "Gender": [data.gender],
        "Country": [data.country],
        "Exercise_hrs_per_week": [data.exercise],
        "Diet_Type": [data.diet],
        "Work_Stress_Level": [data.stress],
        "Medical_History": [data.medical],
        "Smoking": [data.smoking],
        "Alcohol_Consumption": [data.alcohol],
        "Social_Life": [data.social],
        "Sleep_hrs_per_day": [data.sleep],
        "BMI": [data.bmi]
    })

    # Predict life expectancy
    predicted = float(model.predict(input_df)[0])

    # Ensure prediction is not less than current age
    if predicted < data.age:
        predicted = data.age + np.random.uniform(2, 3)

    # Pass all user data including age to LLM for personalized response
    recommendation = generate_llm_recommendations(data.model_dump())

    # Log the message for debugging
    print("=== Generated LLM Initial Message ===")
    print(recommendation)


    # Fallback if LLM fails
    if not recommendation or not recommendation.strip():
        recommendation = "Sorry, we couldn't generate personalized recommendations at this moment."


    return {
        "predicted_life_expectancy": round(predicted, 2),
        "initial_message": recommendation
    }

# Chat endpoint
class ChatRequest(BaseModel):
    user_input: str

@app.post("/chat")
async def chat(request: ChatRequest):
    print("📩 Received chat request:", request.user_input)
    try:
        response = chat_with_bot(request.user_input)
        print("🤖 Responding with:", response)
        return {"chatbot_response": response}
    except Exception as e:
        print("❌ Error in /chat:", e)
        return {"chatbot_response": "Sorry, something went wrong."}
