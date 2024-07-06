import numpy as np
import pandas as pd
import datetime as dt
from flask import Flask, request, jsonify, render_template
import joblib

app = Flask(__name__)
model = joblib.load('model.pkl')
fet = pd.read_csv('all_features.csv')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    features = [x for x in request.form.values()]

    if features[3] == '0':
        features[3] = False
    else:
        features[3] = True

    df = fet[(fet['Store'] == int(features[0])) & (fet['IsHoliday'] == features[3]) & (fet['Date'] == features[2])]
    f_features = []
    d = dt.datetime.strptime(features[2], '%Y-%m-%d')
    c = 0

    # Check if the DataFrame is empty or the 'Type' column is missing
    if df.empty or 'Type' not in df.columns:
        return render_template('index.html', output="Error: Data not found for the given input"), 400

    # Safely access the first element of 'Type' column
    if len(df) > 0 and df['Type'].iloc[0] == 'C':
        c = 1

    if features[3] == False:
        features[3] = 0
    else:
        features[3] = 1

    if df.shape[0] == 1:
        f_features.append(df['CPI'].values[0])
        f_features.append(d.date().day)
        f_features.append(int(features[1]))
        f_features.append(df['Fuel_Price'].values[0])
        f_features.append(features[3])
        f_features.append(d.date().month)
        f_features.append(df['Size'].values[0])
        f_features.append(int(features[0]))
        f_features.append(df['Temperature'].values[0])
        f_features.append(c)
        f_features.append(df['Unemployment'].values[0])
        f_features.append(d.date().year)

    final_features = [np.array(f_features)]
    output = model.predict(final_features)[0]
    return render_template('index.html', output=output)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
