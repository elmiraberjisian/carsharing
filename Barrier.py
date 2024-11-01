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
st.title("Barrier-Action Survey")

st.markdown("""
Please review the list of barrier-action pairs below. If there is any barrier not mentioned, please add it.
If there is an action that can address a barrier, add it too. When you are done, check any actions your
agency can take and submit your response.
""")

# Name input
name = st.text_input("Name and Agency")

# Barrier selection and addition
st.subheader("Add or Select a Barrier")
existing_barrier = st.selectbox("Select Existing Barrier", [""] + list(st.session_state.roadmap.keys()))
new_barrier = st.text_input("Or Enter a New Barrier")

# Action addition
action = st.text_input("Enter Action for Selected Barrier")

# Add Barrier and Action button
if st.button("Add Barrier/Action"):
    if new_barrier:
        if new_barrier not in st.session_state.roadmap:
            st.session_state.roadmap[new_barrier] = []
        if action and action not in st.session_state.roadmap[new_barrier]:
            st.session_state.roadmap[new_barrier].append(action)
    elif existing_barrier and action:
        if action not in st.session_state.roadmap[existing_barrier]:
            st.session_state.roadmap[existing_barrier].append(action)
    st.success("Barrier and/or Action added!")

# Display current roadmap
st.subheader("Current Barrier-Action List")
for barrier, actions in st.session_state.roadmap.items():
    st.write(f"**{barrier}**:")
    for act in actions:
        st.write(f"- {act}")

# Select actions user can take
st.subheader("Select Actions Your Agency Can Take")
selected_actions = []
for barrier, actions in st.session_state.roadmap.items():
    with st.expander(f"{barrier}"):
        selected = st.multiselect(f"Actions for {barrier}", actions)
        selected_actions.extend([(barrier, act) for act in selected])

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
    if not selected_actions:
        st.error("Please select at least one action before submitting.", key="select_action_error")
    elif not name:
        st.error("Please enter your name and agency before submitting.", key="name_error")
    else:
        # Prepare the data for submission
        barriers = [barrier for barrier, action in selected_actions]
        actions = [action for barrier, action in selected_actions]
        
        # Convert selections to DataFrame for storage
        response_data = pd.DataFrame({
            "Name": [name] * len(actions),
            "Barrier": barriers,
            "Action": actions,
            "Comments": [comments] * len(actions)
        })

        # Save the CSV data to a buffer
        csv_buffer = io.StringIO()
        response_data.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()

        # Upload CSV to GitHub
        upload_csv_to_gith
