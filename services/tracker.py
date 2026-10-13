from services.storage import get_db

def get_application(application_id):
    with get_db() as db:
        row = db.execute(
            "SELECT application_id, applicant_name, service_name, status, last_updated, next_step "
            "FROM applications WHERE application_id = ?",
            (application_id.strip().upper(),)
        ).fetchone()
    return dict(row) if row else None
