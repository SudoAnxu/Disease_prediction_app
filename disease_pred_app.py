import streamlit as st
import pickle
import numpy as np
import os
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

# Load ML model
MODEL_PATH = "disease_pred_n.pkl"
with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)

# Disease mapping
disease_mapping = ['Fungal infection', 'Allergy', 'GERD', 'Chronic cholestasis', 'Drug Reaction', 
                   'Peptic ulcer diseae', 'AIDS', 'Diabetes ', 'Gastroenteritis', 'Bronchial Asthma', 
                   'Hypertension ', 'Migraine', 'Cervical spondylosis', 'Paralysis (brain hemorrhage)', 
                   'Jaundice', 'Malaria', 'Chicken pox', 'Dengue', 'Typhoid', 'hepatitis A', 'Hepatitis B', 
                   'Hepatitis C', 'Hepatitis D', 'Hepatitis E', 'Alcoholic hepatitis', 'Tuberculosis', 
                   'Common Cold', 'Pneumonia', 'Dimorphic hemmorhoids(piles)', 'Heart attack', 
                   'Varicose veins', 'Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia', 'Osteoarthristis', 
                   'Arthritis', '(vertigo) Paroymsal  Positional Vertigo', 'Acne', 'Urinary tract infection', 
                   'Psoriasis', 'Impetigo']

# Symptom categories
symptom_categories = {
    "Skin Symptoms": ["itching", "skin_rash", "nodal_skin_eruptions", "blister", "red_sore_around_nose",
                      "yellow_crust_ooze", "scurring", "skin_peeling", "silver_like_dusting",
                      "small_dents_in_nails", "inflammatory_nails", "pus_filled_pimples", "blackheads"],
    "Respiratory Symptoms": ["continuous_sneezing", "cough", "breathlessness", "phlegm", "throat_irritation",
                             "redness_of_eyes", "sinus_pressure", "runny_nose", "congestion", "chest_pain",
                             "mucoid_sputum", "rusty_sputum", "blood_in_sputum"],
    "Digestive Symptoms": ["stomach_pain", "acidity", "ulcers_on_tongue", "vomiting", "burning_micturition",
                           "spotting_ urination", "constipation", "abdominal_pain", "diarrhoea",
                           "loss_of_appetite", "belly_pain", "nausea", "stomach_bleeding",
                           "fluid_overload", "distention_of_abdomen"],
    "General Symptoms": ["shivering", "chills", "fatigue", "weight_gain", "anxiety", "cold_hands_and_feets",
                         "mood_swings", "weight_loss", "restlessness", "lethargy", "high_fever", "sweating",
                         "dehydration", "indigestion", "headache", "yellowish_skin", "dark_urine", "mild_fever",
                         "yellow_urine", "yellowing_of_eyes", "fluid_overload", "malaise",
                         "blurred_and_distorted_vision", "weakness_in_limbs", "fast_heart_rate", "dizziness",
                         "cramps", "bruising", "obesity", "swollen_legs", "swollen_blood_vessels",
                         "puffy_face_and_eyes", "enlarged_thyroid", "brittle_nails", "swollen_extremeties",
                         "excessive_hunger", "drying_and_tingling_lips", "slurred_speech", "muscle_weakness",
                         "loss_of_balance", "unsteadiness", "loss_of_smell", "bladder_discomfort",
                         "foul_smell_of urine", "continuous_feel_of_urine", "passage_of_gases",
                         "internal_itching", "toxic_look_(typhos)", "depression", "irritability", "muscle_pain",
                         "altered_sensorium", "red_spots_over_body", "abnormal_menstruation",
                         "dischromic _patches", "watering_from_eyes", "increased_appetite", "polyuria",
                         "family_history", "lack_of_concentration", "visual_disturbances", "coma",
                         "history_of_alcohol_consumption", "prominent_veins_on_calf", "palpitations",
                         "painful_walking"],
    "Pain Symptoms": ["joint_pain", "muscle_wasting", "pain_behind_the_eyes", "back_pain",
                      "pain_during_bowel_movements", "pain_in_anal_region", "bloody_stool",
                      "irritation_in_anus", "neck_pain", "knee_pain", "hip_joint_pain", "stiff_neck",
                      "swelling_joints", "movement_stiffness", "spinning_movements",
                      "weakness_of_one_body_side"],
    "Other Symptoms": ["patches_in_throat", "irregular_sugar_level", "sunken_eyes", "acute_liver_failure",
                       "swelling_of_stomach", "swelled_lymph_nodes", "extra_marital_contacts",
                       "receiving_blood_transfusion", "receiving_unsterile_injections"]
}

# UI
st.title("🩺 Disease Prediction & Explanation System")

selected_symptoms = []
for category, symptoms in symptom_categories.items():
    selected = st.multiselect(f"Select {category}", symptoms)
    selected_symptoms.extend(selected)

# Convert to binary feature vector
all_symptoms = [symptom for symptoms in symptom_categories.values() for symptom in symptoms]
symptoms_binary = [1 if symptom in selected_symptoms else 0 for symptom in all_symptoms]

# Prediction
if st.button("🔍 Predict Disease"):
    if selected_symptoms:
        try:
            input_array = np.array(symptoms_binary).reshape(1, -1)
            probabilities = model.predict_proba(input_array)
            predicted_index = int(np.argmax(probabilities))
            predicted_disease = disease_mapping[predicted_index]
            confidence = float(np.max(probabilities))

            st.session_state['predicted_disease'] = predicted_disease

            st.success(f"**Predicted Disease:** {predicted_disease}")
            st.info(f"**Confidence Score:** {confidence:.2f}")
        except Exception as e:
            st.error(f"Prediction error: {e}")
    else:
        st.warning("Please select at least one symptom.")

# Explanation
if st.button("💬 Get Explanation"):
    predicted_disease = st.session_state.get("predicted_disease")
    if predicted_disease:
        try:
            prompt_content = (
                f"Explain the following disease in detail:\n"
                f"Disease: {predicted_disease}\n\n"
                f"Please include:\n"
                f"- Common symptoms\n"
                f"- Possible causes\n"
                f"- Recommended treatments and next steps\n"
                f"Please provide a more detailed explanation in natural language."
            )
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful medical assistant that provides detailed explanations for diseases."},
                    {"role": "user", "content": prompt_content}
                ],
                model="llama-3-70b-8192"
            )
            explanation = chat_completion.choices[0].message.content
            st.write("**🧾 Explanation:**")
            st.write(explanation)
        except Exception as e:
            st.error(f"Explanation error: {e}")
    else:
        st.warning("Please run the prediction first to get an explanation.")
