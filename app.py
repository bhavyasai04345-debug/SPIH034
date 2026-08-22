from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    file = request.files['file']
    data = pd.read_csv(file)

    # Simple risk scoring
    data['risk_score'] = (data['days_since_maintenance']*0.5 +
                          data['failure_count']*2 +
                          data['abnormal_readings']*3)

    def classify(score):
        if score < 5: return "Low"
        elif score < 10: return "Medium"
        else: return "High"

    data['risk_level'] = data['risk_score'].apply(classify)
    data['recommendation'] = data['risk_level'].map({
        "High":"Inspect Immediately",
        "Medium":"Calibrate/Monitor",
        "Low":"Routine Maintenance"
    })

    return render_template("results.html", tables=data.to_html(classes='table table-striped', index=False))

if __name__ == "__main__":
    app.run(debug=True)

