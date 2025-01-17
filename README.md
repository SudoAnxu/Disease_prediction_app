# Disease_prediction_app

A Streamlit app with a custom model and LLM to identify diseases from symptoms and provide detailed descriptions.

## Overview

This application leverages machine learning and a language model to predict diseases based on user-input symptoms and offers detailed explanations of the predicted diseases. It is designed to assist users in understanding potential health conditions and recommended next steps.

## Features

- **Symptom Input**: Users can input a list of symptoms.
- **Disease Prediction**: The app predicts the most likely disease based on the symptoms.
- **Detailed Explanation**: Provides a comprehensive explanation of the predicted disease, including common symptoms, possible causes, and recommended treatments.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Git
- Streamlit
- FastAPI
- Required Python packages (listed in `requirements.txt`)

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

4. **Set Up Environment Variables**:
   - Create a `.env` file in the root directory and add your API keys and other sensitive information.

   **Example `.env`**:
   ```plaintext
   GROQ_API_KEY=your_api_key_here
   ```

### Running the Application

1. **Start the FastAPI Backend**:
   ```bash
   uvicorn api_app:app --reload
   ```

2. **Run the Streamlit Frontend**:
   ```bash
   streamlit run streamlit_app.py
   ```

3. **Access the Application**:
   - Open your web browser and go to `http://localhost:8501` to use the app.

## Deployment

### Deploy on Streamlit Cloud

1. **Sign Up or Log In to Streamlit Cloud**: [Streamlit Cloud](https://streamlit.io/cloud)
2. **Create a New App**: Select your GitHub repository and configure the app settings.
3. **Set Up Secrets**: Add any necessary environment variables in the "Secrets" section.
4. **Deploy**: Click "Deploy" to make your app accessible via a public link.

## Usage

- **Input Symptoms**: Use the app interface to input symptoms.
- **Get Predictions**: The app will predict the disease based on the symptoms.
- **Detailed Explanation**: The app provides a detailed explanation of the predicted disease using an LLM.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the Apache 2.0

