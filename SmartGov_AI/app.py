"""Streamlit entry point for the SmartGov AI citizen services app."""

import streamlit as st

from services.assistant import answer_question
from services.dashboard import dashboard_data
from services.grievances import VALID_STATUSES, create_grievance, list_grievances, update_grievance
from services.schemes import search_schemes
from services.storage import init_db
from services.tracker import get_application


st.set_page_config(
    page_title="SmartGov AI | Citizen Services",
    page_icon="🏛️",
    layout="wide",
)

init_db()

st.markdown(
    """
    <style>
    .stApp { background: #f6f9fc; color: #243b53; }
    [data-testid="stHeader"] { background: rgba(246, 249, 252, 0.9); }
    h1, h2, h3 { color: #102a43; }
    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #d9e2ec;
        border-radius: 12px;
        padding: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("SmartGov AI")
st.caption(
    "Citizen Services Portal · Educational prototype — not an official government portal."
)

assistant_tab, schemes_tab, tracker_tab, grievances_tab, dashboard_tab = st.tabs(
    ["Assistant", "Schemes", "Application tracker", "Grievances", "Dashboard"]
)

with assistant_tab:
    st.header("AI Citizen Assistant")
    st.write("Ask about common public services. Answers use curated, keyword-matched FAQs.")
    with st.form("assistant_form"):
        language = st.selectbox("Response language", ["English", "Hindi", "Marathi"])
        question = st.text_area(
            "Your question",
            placeholder="e.g. Where can I find scholarship information?",
        )
        ask = st.form_submit_button("Ask assistant", type="primary")
    if ask:
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            response = answer_question(question.strip(), language)
            st.info(response["answer"])
            st.link_button("Open related official resource", response["source_url"])
            st.caption(response["disclaimer"])

with schemes_tab:
    st.header("Personalized Scheme Finder")
    st.write(
        "Explore scheme information and official portals. Verify current eligibility "
        "and application procedures on each official site."
    )
    with st.form("schemes_form"):
        audience = st.selectbox(
            "I am looking for",
            ["citizen", "student", "farmer", "worker", "business", "all"],
            format_func={
                "citizen": "Any citizen",
                "student": "Student",
                "farmer": "Farmer",
                "worker": "Unorganised worker",
                "business": "Entrepreneur / vendor",
                "all": "All audiences",
            }.get,
        )
        query = st.text_input(
            "Keyword", placeholder="PMJDY, housing, crop insurance, pension, startup..."
        )
        search = st.form_submit_button("Search schemes", type="primary")
    if search:
        results = search_schemes(query, audience)
        if not results:
            st.info("No matching schemes found. Try a different keyword or audience.")
        for scheme in results:
            with st.container(border=True):
                st.subheader(scheme["name"])
                st.write(scheme["description"])
                st.caption(f"Audience: {scheme['audience']}")
                st.write(f"Eligibility: {scheme['eligibility_note']}")
                st.link_button("Open official portal", scheme["official_url"])

with tracker_tab:
    st.header("Smart Application Tracker")
    st.write("Try one of the demo references: SG-1001, SG-1002, or SG-1003.")
    with st.form("tracker_form"):
        application_id = st.text_input(
            "Application reference number", placeholder="SG-1001"
        )
        track = st.form_submit_button("Track application", type="primary")
    if track:
        if not application_id.strip():
            st.warning("Enter an application reference number.")
        else:
            record = get_application(application_id)
            if record is None:
                st.error(
                    "Application not found. This prototype only contains demo records."
                )
            else:
                st.success(f"Status: {record['status']}")
                st.write(f"**Service:** {record['service_name']}")
                st.write(f"**Applicant:** {record['applicant_name']}")
                st.write(f"**Last updated:** {record['last_updated']}")
                st.write(f"**Next step:** {record['next_step']}")

with grievances_tab:
    st.header("Grievance Management")
    st.write(
        "Create a local demo ticket. This prototype does not submit grievances "
        "to government departments."
    )
    with st.form("grievance_form"):
        citizen_name = st.text_input("Name (optional)", placeholder="Demo Citizen")
        locality = st.text_input("Locality (optional)", placeholder="Area or locality")
        description = st.text_area(
            "Describe the issue",
            placeholder="e.g. Water is leaking from the pipeline near my street.",
        )
        submit_grievance = st.form_submit_button(
            "Submit demo grievance", type="primary"
        )
    if submit_grievance:
        if len(description.strip()) < 8:
            st.warning("Please describe the complaint in at least 8 characters.")
        else:
            ticket = create_grievance(
                citizen_name.strip() or "Demo Citizen",
                description.strip(),
                locality.strip(),
            )
            st.success(f"Demo ticket created: {ticket['ticket_id']}")
            st.write(f"**Category:** {ticket['category']}")
            st.write(f"**Department:** {ticket['department']}")
            st.write(f"**Priority:** {ticket['priority']}")
            if ticket["possible_duplicate"]:
                st.info(f"This may be similar to ticket {ticket['possible_duplicate']}.")

    st.subheader("Recent tickets")
    tickets = list_grievances()
    if not tickets:
        st.info("No demo grievances have been submitted.")
    for ticket in tickets:
        with st.container(border=True):
            st.markdown(f"**{ticket['ticket_id']} · {ticket['category']}**")
            st.write(ticket["description"])
            st.caption(
                f"Status: {ticket['status']} · Priority: {ticket['priority']} · "
                f"Department: {ticket['department']}"
            )
            if ticket["locality"]:
                st.caption(f"Locality: {ticket['locality']}")

with dashboard_tab:
    st.header("Smart Governance Dashboard")
    st.caption(
        "Statistics are calculated from local demo records only. "
        "Streamlit Community Cloud storage is ephemeral."
    )
    data = dashboard_data()
    metrics = data["kpis"]
    columns = st.columns(4)
    columns[0].metric("Total applications", metrics["total_applications"])
    columns[1].metric("Pending applications", metrics["pending_applications"])
    columns[2].metric("Total grievances", metrics["total_grievances"])
    columns[3].metric(
        "High-priority recommendations", metrics["high_priority_recommendations"]
    )

    chart_columns = st.columns(2)
    with chart_columns[0]:
        st.subheader("Application statuses")
        statuses = data["application_statuses"]
        if statuses:
            st.bar_chart(
                {
                    "Status": [row["status"] for row in statuses],
                    "Applications": [row["count"] for row in statuses],
                },
                x="Status",
                y="Applications",
            )
        else:
            st.info("No application records.")
    with chart_columns[1]:
        st.subheader("Grievance categories")
        categories = data["grievance_categories"]
        if categories:
            st.bar_chart(
                {
                    "Category": [row["category"] for row in categories],
                    "Grievances": [row["count"] for row in categories],
                },
                x="Category",
                y="Grievances",
            )
        else:
            st.info("No grievance records.")

    st.subheader("Recent grievance tickets")
    recent_tickets = data["recent_grievances"]
    if not recent_tickets:
        st.info("No demo grievance tickets to display.")
    for ticket in recent_tickets:
        with st.form(f"update_{ticket['ticket_id']}"):
            columns = st.columns([1, 1, 1, 1, 1])
            columns[0].write(ticket["ticket_id"])
            columns[1].write(ticket["category"])
            columns[2].write(ticket["priority"])
            selected_status = columns[3].selectbox(
                "Status",
                sorted(VALID_STATUSES),
                index=sorted(VALID_STATUSES).index(ticket["status"]),
                key=f"status_{ticket['ticket_id']}",
                label_visibility="collapsed",
            )
            updated = columns[4].form_submit_button("Update")
            if updated:
                result = update_grievance(ticket["ticket_id"], selected_status)
                if result is None:
                    st.error(f"Could not update ticket {ticket['ticket_id']}.")
                else:
                    st.success(f"Updated {ticket['ticket_id']} to {selected_status}.")
                    st.rerun()
