import streamlit as st
import pandas as pd
import io
import requests
import base64

# GitHub repository details
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]  # Load token from Streamlit Secrets
GITHUB_REPO = "elmiraberjisian/carsharing"  # Replace with your GitHub username and repository name
GITHUB_PATH = "responses/"  # Folder in your repo where CSVs will be stored

# Initialize session state to store the roadmap data
if "roadmap" not in st.session_state:
    st.session_state.roadmap = {
        "Low Market Share": [
            "Targeted outreach and education",
            "Enabling access for rural and remote to transit",
            "Partnering with employees",
            "Placement in residential neighborhoods",
            "Placement near trip generators"
        ],
        "Affordability and Price Predictability": [
            "MaaS integration",
            "Reduced parking requirements"
        ],
        "Temporal and Spatial Availability": [
            "Spatial and temporal demand modeling",
            "Placement in residential neighborhoods",
            "MaaS integration",
            "Placement near transit hubs and frequent transit corridors",
            "Placement near trip generators",
            "Partnering with employees"
        ],
        "Induced Demand and Externalities": [
            "Zero emission fleet",
            "MaaS integration",
            "Placement near transit hubs and frequent transit corridors"
        ],
        "Convenience of Competing Modes": [
            "MaaS integration"
        ],
        "Awareness and Familiarity": [
            "Targeted outreach and education",
            "Placement near transit hubs and frequent transit corridors",
            "Partnering with employees",
            "Placement near trip generators",
            "Placement in residential neighborhoods"
        ],
        "Profitability Operator": [
            "Reduced parking/permit fees"
        ],
        "Fleet Variety": [
            "Zero emission fleet"
        ],
        "Equity": [
            "Subsidized fees for low-income"
        ],
        "Operational Challenges": [
            "Placement near transit hubs and frequent transit corridors",
            "Spatial and temporal demand modeling",
            "Partnering with employees",
            "Placement near trip generators",
            "Placement in residential neighborhoods"
        ]
    }

# Streamlit interface
st.title("Barrier-Opportunity Survey")

st.markdown("""
Please review the list of barrier-opportunity pairs below. If there is any barrier not mentioned, please add it.
If there is an opportunity relevant to a barrier, add it too.
Please use the comment box for any other thoughts particularly regarding road map and scoping.
""")

# Name input
name = st.text_input("Name and Agency")

# Barrier selection and addition
st.subheader("Add or Select a Barrier")
existing_barrier = st.selectbox("Select Existing Barrier", [""] + list(st.session_state.roadmap.keys()))
new_barrier = st.text_input("Or Enter a New Barrier")

# Opportunity addition
opportunity = st.text_input("Enter Opportunity for Selected Barrier")

# Add Barrier and Opportunity button
if st.button("Add Barrier/Opportunity"):
    if new_barrier:
        if new_barrier not in st.session_state.roadmap:
            st.session_state.roadmap[new_barrier] = []
        if opportunity and opportunity not in st.session_state.roadmap[new_barrier]:
            st.session_state.roadmap[new_barrier].append(opportunity)
    elif existing_barrier and opportunity:
        if opportunity not in st.session_state.roadmap[existing_barrier]:
            st.session_state.roadmap[existing_barrier].append(opportunity)
    st.success("Barrier and/or Opportunity added!")

# Display current roadmap
st.subheader("Current Barrier-Opportunity List")
for barrier, opportunities in st.session_state.roadmap.items():
    st.write(f"**{barrier}**:")
    for opp in opportunities:
        st.write(f"- {opp}")

# Comments
comments = st.text_area("Additional Comments or Thoughts")

# Function to upload CSV to GitHub
def upload_csv_to_github(name, csv_data):
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_PATH}{name}_response.csv"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Content-Type": "application/json"
    }
    message = f"Add survey response from {name}"

    # Encode the CSV data as Base64
    content = base64.b64encode(csv_data.encode("utf-8")).decode("utf-8")
    
    data = {
        "message": message,
        "content": content
    }

    response = requests.put(url, headers=headers, json=data)
    if response.status_code == 201:
        st.success("Response submitted and saved to GitHub!")
    else:
        st.error(f"Error uploading to GitHub: {response.status_code}")
        st.error(response.json())

# Submit button
if st.button("Submit Response", key="submit_button"):
    if not name:
        st.error("Please enter name and agency before submitting.")  # Removed `key` parameter and updated message
    else:
        # Prepare the data for submission
        barrier_data = []
        for barrier, opportunities in st.session_state.roadmap.items():
            for opp in opportunities:
                barrier_data.append({"Barrier": barrier, "Opportunity": opp})

        # Convert barrier data to DataFrame for storage
        response_data = pd.DataFrame(barrier_data)
        response_data["Name"] = name
        response_data["Comments"] = comments

        # Save the CSV data to a buffer
        csv_buffer = io.StringIO()
        response_data.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()

        # Upload CSV to GitHub
        upload_csv_to_github(name, csv_data)

        # Display the response for confirmation
        st.write("### Your Submission")
        st.write(response_data)
