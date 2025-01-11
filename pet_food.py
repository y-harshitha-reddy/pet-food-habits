import streamlit as st
import pandas as pd
from PIL import Image
import requests
from io import BytesIO

# Load Excel data
st.sidebar.header("Upload Excel Files")

# Input for Pet Care Data
pet_care_file_path = st.sidebar.text_input("Enter the path for the Pet Care Data file:", "Pet_Care_Data.xlsx")
try:
    pet_care_data = pd.read_excel(pet_care_file_path)
except FileNotFoundError:
    st.error(f"The file `{pet_care_file_path}` was not found. Please ensure the file is in the correct location.")
    st.stop()

# Input for Interesting Facts Data
facts_file_path = st.sidebar.text_input("Enter the path for the Interesting Facts file:", "Interesting_Facts.xlsx")
try:
    facts_data = pd.read_excel(facts_file_path)
except FileNotFoundError:
    st.error(f"The file `{facts_file_path}` was not found. Please ensure the file is in the correct location.")
    st.stop()

# Validate columns for pet care data
pet_care_columns = [
    "Pet Type", "Food Name", "Quantity", "Feeding Time", 
    "Times Per Day", "Types of Food", "Image Path"
]
if not all(col in pet_care_data.columns for col in pet_care_columns):
    st.error("The Pet Care Excel file is missing one or more required columns. Please check the file structure.")
    st.stop()

# Validate columns for interesting facts data
facts_columns = ["Pet Type", "Image Path", "Interesting Facts"]
if not all(col in facts_data.columns for col in facts_columns):
    st.error("The Interesting Facts Excel file is missing one or more required columns. Please check the file structure.")
    st.stop()

# Title
st.title("Pet Care Information System")
st.header("Find the best care routine for your pet and learn fun facts!")

# Sidebar Filters
st.sidebar.header("Filters")

# Filter 1: Pet Type for Care Information
pet_type = st.sidebar.selectbox(
    "Choose a pet for care information:", 
    ["-- Select --"] + pet_care_data["Pet Type"].dropna().unique().tolist()
)

# Filter 2: Pet Type for Interesting Facts
selected_pet_type = st.sidebar.selectbox(
    "Choose a pet to see interesting facts:", 
    ["-- Select --"] + facts_data["Pet Type"].dropna().unique().tolist()
)

# Main Content: Care Information
if pet_type != "-- Select --":
    st.subheader(f"Care Information for {pet_type}s")
    
    # Fetch data for the selected pet type
    pet_info = pet_care_data[pet_care_data["Pet Type"] == pet_type].iloc[0]

    # Display Pet Image
    image_url = pet_info["Image Path"]
    if pd.notna(image_url):
        try:
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
            st.image(image, caption=f"{pet_type}", use_container_width=True)
        except Exception:
            st.warning("Image could not be loaded. Please check the URL.")
    else:
        st.warning("No image URL provided for this pet type.")

    # Display Pet Details
    st.markdown(f"""
    **Food Name:** {pet_info["Food Name"]}  
    **Quantity:** {pet_info["Quantity"]}  
    **Feeding Time:** {pet_info["Feeding Time"]}  
    **Number of Feedings Per Day:** {pet_info["Times Per Day"]}  
    **Types of Food:** {pet_info["Types of Food"]}
    """)

# Main Content: Interesting Facts
if selected_pet_type != "-- Select --":
    st.subheader(f"Interesting Facts about {selected_pet_type}s")
    
    # Fetch facts for the selected pet type
    fact_info = facts_data[facts_data["Pet Type"] == selected_pet_type].iloc[0]
    
    # Display Pet Image
    image_url = fact_info["Image Path"]
    if pd.notna(image_url):
        try:
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
            st.image(image, caption=f"{selected_pet_type}", use_container_width=True)
        except Exception:
            st.warning("Image could not be loaded. Please check the URL.")
    else:
        st.warning("No image URL provided for this pet type.")

    # Display Interesting Facts
    facts = fact_info["Interesting Facts"]
    if pd.notna(facts):
        fact_list = facts.split("|")  # Assuming facts are separated by '|'
        for i, fact in enumerate(fact_list, start=1):
            st.markdown(f"**Fact {i}:** {fact}")
    else:
        st.warning("No interesting facts available for this pet type.")
