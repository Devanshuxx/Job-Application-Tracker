import streamlit as st
import pandas as pd
from datetime import date
import os

# ---------------- CONFIG ---------------- #
st.set_page_config(
    page_title="Job Application Tracker",
    layout="wide"
)

DATA_FILE = "job_applications.csv"

COLUMNS = [
    "Company",
    "Job Title",
    "Location",
    "Salary",
    "Job Type",
    "Date Applied",
    "Source",
    "Update"
]

# ---------------- CUSTOM CSS ---------------- #
st.markdown(
    """
    <style>
    /* Force dark gradient background */
    body, .stApp {
        background: linear-gradient(135deg, #0e1117, #111827) !important;
    }

    /* Main container spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Card-style sections */
    .section-card {
        background-color: #1a1f2b;
        padding: 1.8rem;
        border-radius: 14px;
        margin-bottom: 1.8rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.45);
    }

    /* Applied Jobs heading */
    .applied-heading {
        color: #22c55e;
        font-size: 1.7rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }

    /* NORMAL BUTTONS */
    div.stButton > button {
        background-color: #000000;
        color: #f97316;
        border: 1px solid #f97316;
        border-radius: 8px;
        padding: 0.55rem 1.3rem;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
    }

    /* FORM SUBMIT BUTTON */
    div[data-testid="stFormSubmitButton"] > button {
        background-color: #000000;
        color: #f97316;
        border: 1px solid #f97316;
        border-radius: 8px;
        padding: 0.55rem 1.3rem;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
    }

    /* Hover effect for ALL buttons */
    div.stButton > button:hover,
    div[data-testid="stFormSubmitButton"] > button:hover {
        background-color: #f97316;
        color: #000000;
        transform: translateY(-1px);
    }

    /* Improve label readability */
    label {
        font-weight: 500;
    }
    
    /* Page main heading */
    /* Page main heading */
    h1 {
        color: #f97316 !important;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- DATA HANDLING ---------------- #
def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE, parse_dates=["Date Applied"])
    else:
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(DATA_FILE, index=False)
    return df

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# ---------------- UI ---------------- #
st.title("📌 Job Application Tracker")

df = load_data()

if not df.empty:
    df = df.sort_values(by="Date Applied", ascending=False).reset_index(drop=True)

# ---------------- TABLE SECTION ---------------- #
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="applied-heading">📋 Applied Jobs</div>', unsafe_allow_html=True)

display_df = df.copy()
if not display_df.empty:
    display_df["Date Applied"] = display_df["Date Applied"].dt.date

display_df.insert(0, "Delete", False)

edited_df = st.data_editor(
    display_df,
    use_container_width=True,
    hide_index=True,
    disabled=COLUMNS,
    num_rows="fixed"
)

if st.button("🗑️ Delete Selected Rows"):
    rows_to_delete = edited_df[edited_df["Delete"]].index
    if len(rows_to_delete) == 0:
        st.warning("⚠️ No rows selected for deletion.")
    else:
        df = df.drop(index=rows_to_delete).reset_index(drop=True)
        save_data(df)
        st.success(f"✅ Deleted {len(rows_to_delete)} row(s) successfully!")
        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- ADD FORM SECTION ---------------- #
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("➕ Add New Job Application")

with st.form("job_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)

    with col1:
        company = st.text_input("Company")
        job_title = st.text_input("Job Title")
        location = st.text_input("Location")

    with col2:
        salary = st.text_input("Salary")
        job_type = st.selectbox(
            "Job Type",
            ["Full-Time", "Internship", "Contract", "Remote", "Hybrid", "Other"]
        )
        source = st.text_input("Source")

    with col3:
        date_applied = st.date_input("Date Applied", value=date.today())
        update = st.text_input("Update (Applied / Interview / Rejected / Offer)")

    submitted = st.form_submit_button("Add Details")

    if submitted:
        if company.strip() == "" or job_title.strip() == "":
            st.error("❌ Company and Job Title are required.")
        else:
            new_row = pd.DataFrame([{
                "Company": company,
                "Job Title": job_title,
                "Location": location,
                "Salary": salary,
                "Job Type": job_type,
                "Date Applied": pd.to_datetime(date_applied),
                "Source": source,
                "Update": update
            }])

            df = pd.concat([df, new_row], ignore_index=True)
            save_data(df)

            st.success("✅ Job application added successfully!")
            st.rerun()

st.markdown("</div>", unsafe_allow_html=True)
