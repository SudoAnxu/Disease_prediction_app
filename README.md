
---

# Disease Prediction App

A Streamlit app that uses a custom machine learning model and a language model (LLM) to predict diseases based on symptoms and provide detailed explanations for the predictions.

## Overview

The **Disease Prediction App** leverages machine learning and a language model to predict diseases based on user-input symptoms. It helps users understand potential health conditions by predicting the most likely disease and providing detailed descriptions, including common symptoms, possible causes, and recommended treatments.

## Features

* **Symptom Input**: Users can select symptoms from various categories such as skin, respiratory, digestive, general, pain, and others.
* **Disease Prediction**: The app predicts the most likely disease based on the symptoms selected by the user.
* **Detailed Explanation**: The app offers a detailed explanation of the predicted disease, including common symptoms, possible causes, and recommended treatments.

## Getting Started

### Prerequisites

* Python 3.7 or higher
* Streamlit
* Groq API for detailed explanations
* Required Python packages (listed in `requirements.txt`)

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-username/Disease_prediction_app.git
   cd Disease_prediction_app
   ```

2. **Set Up a Virtual Environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up API Key**:

   * In the root directory of your project, create a `streamlit.toml` file to store your Groq API key.

   **Example `streamlit.toml`**:

   ```toml
   [server]
   headless = true
   port = 8501

   [api]
   GROQ_API_KEY = "your_api_key_here"
   ```

### Running the Application

1. **Run the Streamlit App**:

   ```bash
   streamlit run disease_pred_app.py
   ```

2. **Access the Application**:

   * Open your web browser and navigate to `http://localhost:8501` to interact with the app.

## Deployment

### Deploy on Streamlit Cloud

1. **Sign Up or Log In to Streamlit Cloud**: [Streamlit Cloud](https://streamlit.io/cloud)
2. **Create a New App**: Select your GitHub repository and configure the app settings.
3. **Set Up Secrets**: In Streamlit Cloud, add any necessary environment variables in the "Secrets" section of the app settings.
4. **Deploy**: Click "Deploy" to make your app publicly accessible.

## Usage

* **Input Symptoms**: Use the app's interface to select symptoms from the provided categories.
* **Get Predictions**: Once symptoms are selected, the app will predict the most likely disease and display the confidence score.
* **Get Explanations**: After a prediction, users can click "💬 Get Explanation" to receive a detailed explanation of the predicted disease, including common symptoms, causes, and treatments.

## Working App

Try the working app [here](https://diseasepredictionapp-j9prwxvkgbmtmhprrtuzvi.streamlit.app/).

## Contributing

Contributions are welcome! Feel free to fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the Apache 2.0 License.

---

