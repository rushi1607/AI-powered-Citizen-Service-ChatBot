# SmartGov AI — Government scheme directory and citizen-services demo

A Flask + SQLite educational prototype with a citizen assistant, scheme finder, sample application tracker, local grievance tickets and a demo dashboard. An optional Streamlit interface is also included.

## Government scheme links added
The scheme finder includes PMJDY, PMJJBY, PMSBY, APY, PM-SYM, PMAY, PM SVANidhi, PM Vishwakarma, PMFBY, MUDRA, Startup India, PM-KISAN, UMANG and the National Scholarship Portal. Search by scheme name, keyword or audience.

## Run the Flask website locally
1. Install Python 3.10+.
2. In this folder run: `python -m pip install -r requirements.txt`
3. Start the app: `python app.py`
4. Open `http://127.0.0.1:5000`.

## Optional Streamlit interface
Run `streamlit run streamlit_app.py` to start the separate Streamlit version.

## Deploy the Flask website on Render
1. Push this project to GitHub.
2. In Render, choose **New +** → **Blueprint** and select this repository and the `rushi1607` branch.
3. Render reads the root `render.yaml` file and deploys the Flask site. The public site will use the same interface as `http://127.0.0.1:5000`.

The SQLite database is created and seeded when the app starts. Render's local filesystem can be ephemeral, so demo grievance tickets may be reset when the service restarts or is redeployed.

## Important
This is a demonstration, not an official government portal. Scheme links open official portals for information. Application tracking and grievance tickets are local fictional demo data; they are not connected to government databases and grievances are not submitted to government departments. Always verify eligibility, deadlines, benefits and application procedures on the official portal.
