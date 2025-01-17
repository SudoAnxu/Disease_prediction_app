from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import pickle  # For loading your custom .m5 model
import numpy as np
from groq import Groq as groq  
from dotenv import load_dotenv

# Initialize FastAPI app
app = FastAPI()

# Loading the prediction model
MODEL_PATH = "disease_pred_n.pkl"
with open(MODEL_PATH, "rb") as file:
    custom_model = pickle.load(file)
print(type(custom_model))

# Initialize Groq client with API key
load_dotenv()

# Access the API key
api_key = os.getenv('GROQ_API_KEY')
client = groq(api_key=api_key)

# Define input schema
class SymptomInput(BaseModel):
    symptoms: list[float]  # Binary feature values
class DiseaseRequest(BaseModel):
    predicted_disease: str

# Root Endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Disease Prediction API!"}

# Prediction Endpoint
disease_mapping = ['Fungal infection', 'Allergy', 'GERD', 'Chronic cholestasis', 'Drug Reaction', 'Peptic ulcer diseae', 'AIDS', 'Diabetes ', 'Gastroenteritis', 'Bronchial Asthma', 'Hypertension ', 'Migraine', 'Cervical spondylosis', 'Paralysis (brain hemorrhage)', 'Jaundice', 'Malaria', 'Chicken pox', 'Dengue', 'Typhoid', 'hepatitis A', 'Hepatitis B', 'Hepatitis C', 'Hepatitis D', 'Hepatitis E', 'Alcoholic hepatitis', 'Tuberculosis', 'Common Cold', 'Pneumonia', 'Dimorphic hemmorhoids(piles)', 'Heart attack', 'Varicose veins', 'Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia', 'Osteoarthristis', 'Arthritis', '(vertigo) Paroymsal  Positional Vertigo', 'Acne', 'Urinary tract infection', 'Psoriasis', 'Impetigo']
@app.post("/predict")
def predict_disease(input_data: SymptomInput):
    try:
        # Convert input to numpy array
        symptoms_array = np.array(input_data.symptoms).reshape(1, -1)
       

        # Using my model for predictions
        predictions = custom_model.predict_proba(symptoms_array)
    
        predicted_class = int(np.argmax(predictions))
        predicted_disease_name = disease_mapping[predicted_class]
        confidence_score = float(np.max(predictions))

        return {
            "predicted_disease": predicted_disease_name,
            "confidence_score": confidence_score
        }
    except Exception as e:
        print(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Error during prediction: {str(e)}")

# Explanation Endpoint
@app.post("/explain")
def explain_disease(request: DiseaseRequest):
    try:
        predicted_disease = request.predicted_disease
       

        # Construct a prompt for the LLM using the predicted disease
        prompt_content = (
            f"Explain the following disease in detail:\n"
            f"Disease: {predicted_disease}\n\n"
            f"Please include:\n"
            f"- Common symptoms\n"
            f"- Possible causes\n"
            f"- Recommended treatments and next steps\n"
            f"Please provide a more detailed explanation in natural language."
        )
       

        # Call the LLM for generating the explanation
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful medical assistant that provides detailed explanations for diseases."
                },
                {
                    "role": "system",
                    "content": prompt_content,
                }
            ],
            model="llama-3.3-70b-versatile",
        )

      
    
        return {
            "explanation": {
                "predicted_disease": predicted_disease,
                "detailed_explanation": chat_completion.choices[0].message.content
            }
        }
    except Exception as e:
        print(f"Error during explanation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error during explanation: {str(e)}")