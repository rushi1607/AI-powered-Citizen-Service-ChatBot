# SmartGov AI — Government scheme directory and citizen-services demo

A Flask/Streamlit + SQLite educational prototype with a citizen assistant, scheme finder, sample application tracker, local grievance tickets and a demo dashboard.

## Government scheme links added
The scheme finder includes PMJDY, PMJJBY, PMSBY, APY, PM-SYM, PMAY, PM SVANidhi, PM Vishwakarma, PMFBY, MUDRA, Startup India, PM-KISAN, UMANG and the National Scholarship Portal. Search by scheme name, keyword or audience.

## Run locally with Streamlit
1. Install Python 3.10+.
2. In this folder run: `python -m pip install -r requirements.txt`
3. Start the app: `streamlit run streamlit_app.py`
4. Open the local URL shown in the terminal.

## Run locally with Flask
1. Install the dependencies: `python -m pip install -r requirements.txt`
2. Initialize the database: `python -m services.storage`
3. Start the site: `python app.py`
4. Open `http://127.0.0.1:5000`.

## Deploy on Streamlit Community Cloud
1. Push this project to a GitHub repository.
2. In Streamlit Community Cloud, create an app from the repository and select the `rushi1607` branch.
3. Set the app file path to `SmartGov_AI/streamlit_app.py` and deploy.

The SQLite database is created and seeded when the app starts. On Streamlit Community Cloud, its writable filesystem is ephemeral; demo grievance tickets can be reset when the app restarts or is redeployed.

## Important
This is a demonstration, not an official government portal. Scheme links open official portals for information. Application tracking and grievance tickets are local fictional demo data; they are not connected to government databases and grievances are not submitted to government departments. Always verify eligibility, deadlines, benefits and application procedures on the official portal.
