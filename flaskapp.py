# -*- coding: utf-8 -*-
"""FlaskApp.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1l2Roa6N30OoSiyZ_vOpF-m3xQaoHah4r
"""

from flask import Flask, request, jsonify
import joblib
import os
import urllib.request  # For optional remote model loading

app = Flask(__name__)

# ====== Updated Model Loading ======
MODEL_FILENAME = "crop_model.joblib"
MODEL_PATH = os.path.join(os.path.dirname(__file__), MODEL_FILENAME)

# Option 1: Load from local file (preferred for Render)
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    # Option 2: Download from alternative source (if needed)
    try:
        MODEL_URL = "https://github.com/Jason1576/soil-analysis-api/raw/refs/heads/main/crop_model.joblibb"  
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
        model = joblib.load(MODEL_PATH)
    except Exception as e:
        raise RuntimeError(f"Failed to load model: {str(e)}")

# ====== Prediction Endpoint ======
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        required = ["N", "P", "K", "temp", "humidity", "ph"]
        if not all(key in data for key in required):
            return jsonify({"error": "Missing fields"}), 400

        features = [data[key] for key in required]
        prediction = model.predict([features])[0]
        return jsonify({"crop": prediction})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ====== Main Execution ======
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # For Render compatibility
    app.run(host='0.0.0.0', port=port)
