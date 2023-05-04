import pandas as pd
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


data = pd.read_csv("data.csv")
info_df = pd.read_csv("info_about_data.csv")


@app.route("/")
def index():
    questions = {row["Question_id"]: row["Text"] for _, row in info_df.iterrows()}
    return render_template("index.html", questions=questions)


@app.route("/calculate_mean", methods=["POST"])
def calculate_mean():
    q_binary = request.json["selectedQuestion"]
    grouped_data = data.groupby("hospital")
    means = grouped_data[q_binary.lower()].mean()
    response_data = {}
    for hospital, mean in means.items():
        response_data[hospital] = mean
    return jsonify(response_data)


if __name__ == "__main__":
    app.run(debug=True)
