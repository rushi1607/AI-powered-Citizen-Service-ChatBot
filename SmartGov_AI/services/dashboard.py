from services.storage import get_db

def dashboard_data():
    with get_db() as db:
        total_apps = db.execute("SELECT COUNT(*) FROM applications").fetchone()[0]
        pending_apps = db.execute(
            "SELECT COUNT(*) FROM applications WHERE status != 'Approved'"
        ).fetchone()[0]
        total_grievances = db.execute("SELECT COUNT(*) FROM grievances").fetchone()[0]
        high_priority = db.execute(
            "SELECT COUNT(*) FROM grievances WHERE priority LIKE 'High%'"
        ).fetchone()[0]
        app_rows = db.execute(
            "SELECT status, COUNT(*) AS count FROM applications GROUP BY status"
        ).fetchall()
        grievance_rows = db.execute(
            "SELECT category, COUNT(*) AS count FROM grievances GROUP BY category"
        ).fetchall()
        recent = db.execute(
            "SELECT ticket_id, category, priority, department, status, created_at "
            "FROM grievances ORDER BY id DESC LIMIT 10"
        ).fetchall()
    return {
        "kpis": {
            "total_applications": total_apps,
            "pending_applications": pending_apps,
            "total_grievances": total_grievances,
            "high_priority_recommendations": high_priority
        },
        "application_statuses": [dict(r) for r in app_rows],
        "grievance_categories": [dict(r) for r in grievance_rows],
        "recent_grievances": [dict(r) for r in recent],
        "disclaimer": "All figures are from this local prototype database, not live government systems."
    }
