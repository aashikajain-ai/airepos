from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["finance_db"]
transactions_collection = db["transactions"]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add", methods=["POST"])
def add_transaction():
    try:
        transaction = {
            "date": request.form.get("date"),
            "type": request.form.get("type", "").strip().lower(),
            "category": request.form.get("category"),
            "amount": float(request.form.get("amount", 0))
        }

        if not all([transaction["date"], transaction["type"], transaction["category"]]):
            return redirect(url_for("home"))

        transactions_collection.insert_one(transaction)
        return redirect(url_for("home"))

    except (ValueError, TypeError):
        return redirect(url_for("home"))


@app.route("/dashboard")
def dashboard():
    transactions = list(transactions_collection.find({}, {"_id": 0}))
    df = pd.DataFrame(transactions)

    if df.empty:
        return render_template(
            "dashboard.html",
            income=0,
            expense=0,
            savings=0,
            category_data={},
            cluster_data=[]
        )

    income_total = df[df["type"] == "income"]["amount"].sum()
    expense_total = df[df["type"] == "expense"]["amount"].sum()
    savings_total = income_total - expense_total

    expense_df = df[df["type"] == "expense"].copy()
    category_data = {}
    cluster_data = []

    if not expense_df.empty:
        category_summary = expense_df.groupby("category")["amount"].sum()
        category_data = {k: float(v) for k, v in category_summary.to_dict().items()}

    if len(expense_df) >= 3:
        try:
            scaler = StandardScaler()
            scaled_amounts = scaler.fit_transform(expense_df[["amount"]])

            kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
            expense_df["cluster"] = kmeans.fit_predict(scaled_amounts)

            cluster_data = expense_df[["amount", "cluster"]].to_dict(orient="records")

        except Exception:
            cluster_data = []

    return render_template(
        "dashboard.html",
        income=float(income_total),
        expense=float(expense_total),
        savings=float(savings_total),
        category_data=category_data,
        cluster_data=cluster_data
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)