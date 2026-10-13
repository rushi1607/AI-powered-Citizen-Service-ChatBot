"""Original Flask API and website entry point."""

from flask import Flask, request, jsonify, render_template
from services.storage import init_db
from services.assistant import answer_question
from services.schemes import search_schemes
from services.tracker import get_application
from services.grievances import create_grievance, list_grievances, update_grievance
from services.dashboard import dashboard_data

app = Flask(__name__)

@app.get("/")
def home():
    return render_template("index.html")

@app.post("/api/assistant")
def assistant_api():
    data = request.get_json(silent=True) or {}
    question = (data.get("question") or "").strip()
    language = (data.get("language") or "English").strip()
    if not question:
        return jsonify({"error": "Please enter a question."}), 400
    return jsonify(answer_question(question, language))

@app.post("/api/schemes")
def schemes_api():
    data = request.get_json(silent=True) or {}
    query = (data.get("query") or "").strip()
    audience = (data.get("audience") or "citizen").strip().lower()
    return jsonify({"results": search_schemes(query, audience)})

@app.get("/api/applications/<application_id>")
def tracker_api(application_id):
    record = get_application(application_id)
    if not record:
        return jsonify({"error": "Application not found. This prototype only contains demo records."}), 404
    return jsonify(record)

@app.post("/api/grievances")
def create_grievance_api():
    data = request.get_json(silent=True) or {}
    name = (data.get("citizen_name") or "Demo Citizen").strip()
    description = (data.get("description") or "").strip()
    locality = (data.get("locality") or "").strip()
    if len(description) < 8:
        return jsonify({"error": "Please describe the complaint in at least 8 characters."}), 400
    return jsonify(create_grievance(name, description, locality)), 201

@app.get("/api/grievances")
def list_grievances_api():
    return jsonify({"grievances": list_grievances()})

@app.patch("/api/grievances/<ticket_id>")
def update_grievance_api(ticket_id):
    data = request.get_json(silent=True) or {}
    status = (data.get("status") or "").strip()
    result = update_grievance(ticket_id, status)
    if not result:
        return jsonify({"error": "Ticket not found or status is invalid."}), 404
    return jsonify(result)

@app.get("/api/dashboard")
def dashboard_api():
    return jsonify(dashboard_data())

if __name__ == "__main__":
    init_db()
    app.run(debug=True, use_reloader=False)
