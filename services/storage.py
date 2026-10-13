import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "smartgov.db"

def get_db():
    connection = sqlite3.connect(str(DATABASE_PATH))
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                application_id TEXT UNIQUE NOT NULL,
                applicant_name TEXT NOT NULL,
                service_name TEXT NOT NULL,
                status TEXT NOT NULL,
                last_updated TEXT NOT NULL,
                next_step TEXT NOT NULL
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS schemes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                audience TEXT NOT NULL,
                keywords TEXT NOT NULL,
                official_url TEXT NOT NULL,
                eligibility_note TEXT NOT NULL
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS grievances (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id TEXT UNIQUE NOT NULL,
                citizen_name TEXT NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                priority TEXT NOT NULL,
                department TEXT NOT NULL,
                locality TEXT DEFAULT '',
                status TEXT NOT NULL,
                possible_duplicate TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        applications = [
            ("SG-1001", "Demo Citizen", "Income Certificate", "Under Review", "2026-10-10", "Check the relevant department for further updates."),
            ("SG-1002", "Demo Citizen", "Residence Certificate", "Approved", "2026-10-09", "Follow the issuing authority instructions for collection."),
            ("SG-1003", "Demo Citizen", "Student Assistance", "Pending Documents", "2026-10-08", "Review the document requirements before proceeding.")
        ]
        db.executemany("""
            INSERT OR IGNORE INTO applications
            (application_id, applicant_name, service_name, status, last_updated, next_step)
            VALUES (?, ?, ?, ?, ?, ?)
        """, applications)
        schemes = [
            ("National Scholarship Portal", "Explore scholarship opportunities and application resources.", "student", "scholarship education student financial assistance", "https://scholarships.gov.in/", "Eligibility depends on the specific scholarship and its official guidelines."),
            ("PM-KISAN", "Access information about the PM-KISAN farmer income support scheme.", "farmer", "farmer agriculture income support pm kisan", "https://pmkisan.gov.in/", "Check the current official eligibility rules and exclusions."),
            ("UMANG", "Discover digital public services through the UMANG platform.", "citizen", "citizen government services digital documents", "https://web.umang.gov.in/", "Service availability and eligibility vary by service."),
            ("Pradhan Mantri Jan Dhan Yojana (PMJDY)", "Financial inclusion scheme providing access to basic banking and related services.", "citizen", "bank account financial inclusion pmjdy jan dhan money", "https://pmjdy.gov.in/scheme", "Confirm account and benefit conditions with the official portal or participating bank."),
            ("Pradhan Mantri Jeevan Jyoti Bima Yojana (PMJJBY)", "Renewable life insurance scheme offered through participating banks and post offices.", "citizen", "life insurance pmjjby social security", "https://jansuraksha.gov.in/", "Review current age, premium, enrolment and claim rules on the official portal."),
            ("Pradhan Mantri Suraksha Bima Yojana (PMSBY)", "Affordable accident insurance scheme available through participating institutions.", "citizen", "accident insurance pmsby social security", "https://jansuraksha.gov.in/", "Check current eligibility, premium and coverage terms before enrolment."),
            ("Atal Pension Yojana (APY)", "Pension scheme for eligible subscribers to support income security in old age.", "citizen", "pension apy old age social security", "https://www.npscra.nsdl.co.in/scheme-details.php", "Eligibility and contribution amounts depend on current scheme rules."),
            ("Pradhan Mantri Shram Yogi Maandhan (PM-SYM)", "Pension scheme information for eligible workers in the unorganised sector.", "worker", "pm sym pension worker unorganised trader social security", "https://maandhan.in/", "Check the official portal for current age, income and enrolment requirements."),
            ("Pradhan Mantri Awas Yojana (PMAY)", "Official housing scheme information for eligible urban and rural households.", "citizen", "housing house home pmay awas urban rural", "https://pmay-urban.gov.in/", "Scheme components and application routes vary; check the relevant official portal."),
            ("PM SVANidhi", "Working-capital support information for eligible street vendors.", "business", "street vendor loan working capital pmsvanidhi business", "https://pmsvanidhi.mohua.gov.in/", "Check the official portal for current lending and eligibility conditions."),
            ("PM Vishwakarma", "Support for eligible traditional artisans and craftspeople, including skills and toolkit support.", "business", "artisan craftspeople skill toolkit vishwakarma traditional", "https://pmvishwakarma.gov.in/", "Eligible trades and benefits are defined by the official scheme guidelines."),
            ("Pradhan Mantri Fasal Bima Yojana (PMFBY)", "Crop insurance scheme information for farmers.", "farmer", "crop insurance farming pmfby agriculture", "https://pmfby.gov.in/", "Crop, season, state and enrolment deadlines may vary; verify current notices."),
            ("Pradhan Mantri MUDRA Yojana (PMMY)", "Information on loans for eligible micro and small non-farm enterprises through lending institutions.", "business", "mudra loan micro small business entrepreneur pmmy", "https://www.mudra.org.in/", "Loan approval and terms are decided by the lending institution."),
            ("Startup India", "Government initiative offering resources and guidance for startup recognition and ecosystem support.", "business", "startup india entrepreneur new business funding recognition", "https://www.startupindia.gov.in/", "Benefits have separate eligibility criteria; review current official guidelines.")
        ]
        for item in schemes:
            db.execute("""
                INSERT INTO schemes (name, description, audience, keywords, official_url, eligibility_note)
                SELECT ?, ?, ?, ?, ?, ?
                WHERE NOT EXISTS (SELECT 1 FROM schemes WHERE name = ?)
            """, (*item, item[0]))
        db.commit()

if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {DATABASE_PATH}")
