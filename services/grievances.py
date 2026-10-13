from datetime import datetime
import re
from services.storage import get_db

VALID_STATUSES = {"Submitted", "In Progress", "Resolved", "Closed"}

def classify_grievance(description):
    text = description.lower()
    rules = [
        (["water", "leak", "pipeline", "drinking water"], "Water Supply", "Water Department"),
        (["garbage", "waste", "cleanliness", "drain", "sewage"], "Sanitation", "Municipal Sanitation"),
        (["road", "pothole", "streetlight", "street light"], "Roads and Infrastructure", "Public Works Department"),
        (["electricity", "power cut", "electric"], "Electricity", "Electricity Department"),
        (["pension", "benefit", "payment"], "Welfare Benefits", "Social Welfare Department"),
    ]
    for keywords, category, department in rules:
        if any(k in text for k in keywords):
            return category, department
    return "General", "Public Grievance Office"

def create_grievance(citizen_name, description, locality=""):
    category, department = classify_grievance(description)
    urgent_terms = ["urgent", "emergency", "danger", "hazard", "life-threatening"]
    priority = "High (review recommended)" if any(term in description.lower() for term in urgent_terms) else "Normal (review recommended)"
    now = datetime.now().isoformat(timespec="seconds")
    normalized = re.sub(r"\W+", " ", description.lower()).strip()
    duplicate = None
    with get_db() as db:
        recent = db.execute(
            "SELECT ticket_id, description FROM grievances ORDER BY id DESC LIMIT 100"
        ).fetchall()
        for row in recent:
            previous = re.sub(r"\W+", " ", row["description"].lower()).strip()
            if normalized and (normalized == previous or normalized in previous or previous in normalized):
                duplicate = row["ticket_id"]
                break
        count = db.execute("SELECT COUNT(*) FROM grievances").fetchone()[0] + 1
        ticket_id = f"GR-{2000 + count}"
        db.execute("""
            INSERT INTO grievances
            (ticket_id, citizen_name, description, category, priority, department,
             locality, status, possible_duplicate, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (ticket_id, citizen_name or "Demo Citizen", description, category, priority,
              department, locality, "Submitted", duplicate, now, now))
        db.commit()
        row = db.execute("SELECT * FROM grievances WHERE ticket_id = ?", (ticket_id,)).fetchone()
    return dict(row)

def list_grievances():
    with get_db() as db:
        rows = db.execute("SELECT * FROM grievances ORDER BY id DESC").fetchall()
    return [dict(row) for row in rows]

def update_grievance(ticket_id, status):
    if status not in VALID_STATUSES:
        return None
    now = datetime.now().isoformat(timespec="seconds")
    with get_db() as db:
        cursor = db.execute(
            "UPDATE grievances SET status = ?, updated_at = ? WHERE ticket_id = ?",
            (status, now, ticket_id)
        )
        db.commit()
        if cursor.rowcount == 0:
            return None
        row = db.execute("SELECT * FROM grievances WHERE ticket_id = ?", (ticket_id,)).fetchone()
    return dict(row)
