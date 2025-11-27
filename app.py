from flask import Flask, request, jsonify, render_template
import sqlite3
import os

app = Flask(__name__)


# ---------------- DATABASE SETUP ----------------
def create_table():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS internships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            duration TEXT NOT NULL,
            stipend TEXT
        )
    ''')
    conn.commit()
    conn.close()


def insert_sample_data():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM internships")
    count = cur.fetchone()[0]

    if count == 0:
        sample_data = [
            ("Python Developer Intern", "Google", "3 Months", "8000"),
            ("Web Developer Intern", "Microsoft", "2 Months", "10000"),
            ("Data Analyst Intern", "TCS", "6 Months", "12000"),
        ]

        for title, company, duration, stipend in sample_data:
            cur.execute(
                "INSERT INTO internships (title, company, duration, stipend) VALUES (?, ?, ?, ?)",
                (title, company, duration, stipend),
            )

        conn.commit()

    conn.close()


create_table()
insert_sample_data()


# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template("index.html")


# GET internships with optional filtering
@app.route("/api/internships", methods=["GET"])
def get_internships():
    company_filter = request.args.get("company")
    duration_filter = request.args.get("duration")

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    query = "SELECT * FROM internships WHERE 1=1"
    params = []

    if company_filter:
        query += " AND company = ?"
        params.append(company_filter)

    if duration_filter:
        query += " AND duration = ?"
        params.append(duration_filter)

    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()

    data = [
        {"id": r[0], "title": r[1], "company": r[2], "duration": r[3], "stipend": r[4]}
        for r in rows
    ]
    return jsonify(data)


# ADD internship
@app.route("/api/internships", methods=["POST"])
def add_internship():
    data = request.json
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO internships (title, company, duration, stipend) VALUES (?, ?, ?, ?)",
        (data["title"], data["company"], data["duration"], data.get("stipend")),
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Internship added successfully"}), 201


# UPDATE internship
@app.route("/api/internships/<int:id>", methods=["PUT"])
def update_internship(id):
    data = request.json
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute(
        "UPDATE internships SET title=?, company=?, duration=?, stipend=? WHERE id=?",
        (
            data["title"],
            data["company"],
            data["duration"],
            data.get("stipend"),
            id,
        ),
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Internship updated successfully"})


# DELETE internship
@app.route("/api/internships/<int:id>", methods=["DELETE"])
def delete_internship(id):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM internships WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Internship deleted successfully"})


if __name__ == "__main__":
    app.run(debug=True)
