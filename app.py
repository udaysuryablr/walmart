import numpy as np
import pandas as pd
import datetime as dt
from flask import Flask, request, render_template
import joblib

app = Flask(__name__)

# Load the trained model and feature data
model = joblib.load('model.pkl')
fet = pd.read_csv('all_features.csv')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    features = [x for x in request.form.values()]

    if len(features) != 4:
        return render_template('index.html', output="Error: Incomplete data input"), 400

    try:
        store_id = int(features[0])
        dept_id = int(features[1])
        date_str = features[2]
        is_holiday = bool(int(features[3]))

        # Ensure the date is in the correct format
        try:
            d = dt.datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            return render_template('index.html', output="Error: Invalid date format. Use YYYY-MM-DD."), 400

        # Extract features from the dataset
        df = fet[(fet['Store'] == store_id) & (fet['IsHoliday'] == is_holiday) & (fet['Date'] == date_str)]
        
        if df.empty or 'Type' not in df.columns:
            return render_template('index.html', output="Error: Data not found for the given input"), 400
        
        # Determine whether the type is 'C'
        c = 0 if df['Type'].iloc[0] != 'C' else 1

        # Prepare the features for the model
        f_features = [
            df['CPI'].values[0],
            d.date().day,
            dept_id,
            df['Fuel_Price'].values[0],
            is_holiday,
            d.date().month,
            df['Size'].values[0],
            store_id,
            df['Temperature'].values[0],
            c,
            df['Unemployment'].values[0],
            d.date().year
        ]

        final_features = [np.array(f_features)]
        output = model.predict(final_features)[0]

        return render_template('index.html', output=f"${output:,.2f}")

    except Exception as e:
        return render_template('index.html', output=f"Error: {str(e)}"), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

