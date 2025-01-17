import streamlit as st
import requests

# Grouping symptoms into categories
symptom_categories = {
    "Skin Symptoms": [
        "itching",
        "skin_rash",
        "nodal_skin_eruptions",
        "blister",
        "red_sore_around_nose",
        "yellow_crust_ooze",
        "scurring",
        "skin_peeling",
        "silver_like_dusting",
        "small_dents_in_nails",
        "inflammatory_nails",
        "pus_filled_pimples",
        "blackheads"
    ],
    "Respiratory Symptoms": [
        "continuous_sneezing",
        "cough",
        "breathlessness",
        "phlegm",
        "throat_irritation",
        "redness_of_eyes",
        "sinus_pressure",
        "runny_nose",
        "congestion",
        "chest_pain",
        "mucoid_sputum",
        "rusty_sputum",
        "blood_in_sputum"
    ],
    "Digestive Symptoms": [
        "stomach_pain",
        "acidity",
        "ulcers_on_tongue",
        "vomiting",
        "burning_micturition",
        "spotting_ urination",
        "constipation",
        "abdominal_pain",
        "diarrhoea",
        "loss_of_appetite",
        "belly_pain",
        "nausea",
        "stomach_bleeding",
        "fluid_overload",
        "distention_of_abdomen"
    ],
    "General Symptoms": [
        "shivering",
        "chills",
        "fatigue",
        "weight_gain",
        "anxiety",
        "cold_hands_and_feets",
        "mood_swings",
        "weight_loss",
        "restlessness",
        "lethargy",
        "high_fever",
        "sweating",
        "dehydration",
        "indigestion",
        "headache",
        "yellowish_skin",
        "dark_urine",
        "mild_fever",
        "yellow_urine",
        "yellowing_of_eyes",
        "fluid_overload",
        "malaise",
        "blurred_and_distorted_vision",
        "weakness_in_limbs",
        "fast_heart_rate",
        "dizziness",
        "cramps",
        "bruising",
        "obesity",
        "swollen_legs",
        "swollen_blood_vessels",
        "puffy_face_and_eyes",
        "enlarged_thyroid",
        "brittle_nails",
        "swollen_extremeties",
        "excessive_hunger",
        "drying_and_tingling_lips",
        "slurred_speech",
        "muscle_weakness",
        "loss_of_balance",
        "unsteadiness",
        "loss_of_smell",
        "bladder_discomfort",
        "foul_smell_of urine",
        "continuous_feel_of_urine",
        "passage_of_gases",
        "internal_itching",
        "toxic_look_(typhos)",
        "depression",
        "irritability",
        "muscle_pain",
        "altered_sensorium",
        "red_spots_over_body",
        "abnormal_menstruation",
        "dischromic _patches",
        "watering_from_eyes",
        "increased_appetite",
        "polyuria",
        "family_history",
        "lack_of_concentration",
        "visual_disturbances",
        "coma",
        "history_of_alcohol_consumption",
        "prominent_veins_on_calf",
        "palpitations",
        "painful_walking"
    ],
    "Pain Symptoms": [
        "joint_pain",
        "muscle_wasting",
        "pain_behind_the_eyes",
        "back_pain",
        "pain_during_bowel_movements",
        "pain_in_anal_region",
        "bloody_stool",
        "irritation_in_anus",
        "neck_pain",
        "knee_pain",
        "hip_joint_pain",
        "stiff_neck",
        "swelling_joints",
        "movement_stiffness",
        "spinning_movements",
        "weakness_of_one_body_side"
    ],
    "Other Symptoms": [
        "patches_in_throat",
        "irregular_sugar_level",
        "sunken_eyes",
        "acute_liver_failure",
        "swelling_of_stomach",
        "swelled_lymph_nodes",
        "extra_marital_contacts",
        "receiving_blood_transfusion",
        "receiving_unsterile_injections"
    ]
}

# Setting up the Streamlit app
st.title("Disease Prediction Chat Interface")

# Collect selected symptoms from each category
selected_symptoms = []
for category, symptoms in symptom_categories.items():
    selected = st.multiselect(f"Select {category}", symptoms)
    selected_symptoms.extend(selected)

# Convert selected symptoms to binary feature values
all_symptoms = [symptom for symptoms in symptom_categories.values() for symptom in symptoms]
symptoms_binary = [1 if symptom in selected_symptoms else 0 for symptom in all_symptoms]


# Button for prediction
if st.button("Predict"):
    if selected_symptoms:
        # Send symptoms to the FastAPI predict endpoint
        try:
            response = requests.post(
                "http://127.0.0.1:8000/predict",
                json={"symptoms": symptoms_binary}
            )
            response_data = response.json()

            # Store the predicted disease in session state
            st.session_state['predicted_disease'] = response_data['predicted_disease']

            # Display the predicted disease and confidence score
            st.write(f"**Predicted Disease:** {st.session_state['predicted_disease']}")
            st.write(f"**Confidence Score:** {response_data['confidence_score']:.2f}")

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please select at least one symptom to predict.")

# Button for explanation
if st.button("Get Explanation"):
    if st.session_state.get('predicted_disease'):
        try:
            # Send the predicted disease to the FastAPI explain endpoint
            explanation_response = requests.post(
                "http://127.0.0.1:8000/explain",
                json={"predicted_disease": st.session_state['predicted_disease']}
            )
            explanation_data = explanation_response.json()

            # Display the explanation
            detailed_explanation = explanation_data.get('explanation', {}).get('detailed_explanation', "No explanation available.")
            st.write("**Explanation:**")
            st.write(detailed_explanation)

        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to the explanation service: {e}")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please predict a disease first to get an explanation.")