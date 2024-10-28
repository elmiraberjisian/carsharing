import streamlit as st
import pandas as pd

# Initialize session state to store the roadmap data
if "roadmap" not in st.session_state:
    st.session_state.roadmap = {
        "Small Market Share": [
            "Tiered/predictable pricing packages",
            "Ensuring spatial accessibility throughout the region",
            "Reduced residential parking requirements",
            "Placing vehicles within/nearby residence locations"
        ],
        "Induced Demand/Externality": [
            "Zero emission fleet",
            "Integration into MaaS",
            "Placing vehicles in frequent transit corridors",
            "Placing vehicles in TOD"
        ],
        "Equity": [
            "Targeted outreach",
            "Low-income pass"
        ],
        "Operational Challenges": [
            "Placing vehicles in frequent transit corridors",
            "Placing vehicles in TOD",
            "Spatial-temporal demand models"
        ],
        "Accessibility": [
            "Placing vehicles within/nearby residence locations",
            "Ensuring spatial accessibility throughout the region",
            "Placing vehicles in frequent transit corridors",
            "Placing vehicles near trip generators (health care facilities, businesses, universities)",
            "Spatial-temporal demand models"
        ],
        "Profitability": [
            "Waiving/reduced parking fees",
            "Spatial-temporal demand models",
            "Reduced insurance fees"
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
        # Add new barrier
        if new_barrier not in st.session_state.roadmap:
            st.session_state.roadmap[new_barrier] = []
        # Add action to the new barrier
        if action and action not in st.session_state.roadmap[new_barrier]:
            st.session_state.roadmap[new_barrier].append(action)
    elif existing_barrier and action:
        # Add action to the selected existing barrier
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

# Submit button
if st.button("Submit Response"):
    # Check if there is at least one action selected
    if not selected_actions:
        st.error("Please select at least one action before submitting.")
    elif not name:
        st.error("Please enter your name and agency before submitting.")
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

        # Save the response to a CSV file
        response_data.to_csv(f"{name}_response.csv", index=False)
        st.success("Your response has been submitted and saved!")

        # Display the response for confirmation
        st.write("### Your Submission")
        st.write(response_data)

    st.write(response_data)
