import streamlit as st
import pandas as pd
from PIL import Image
import requests
from io import BytesIO

# Load Excel data
excel_file_path = "Pet_Care_Data.xlsx"
facts_excel_file_path = "Interesting_Facts.xlsx"  # Additional Excel for interesting facts
pet_data = pd.read_excel(excel_file_path)
facts_data = pd.read_excel(facts_excel_file_path)

# Title
st.title("Pet Care Information System")
st.header("Find the best care routine for your pet!")

# Sidebar Filter for Pet Type
st.sidebar.header("Select Pet Type")
pet_type = st.sidebar.selectbox(
    "Choose a pet:", 
    ["-- Select --"] + pet_data["Pet Type"].tolist()
)

# Additional Filter for Pet Names and Interesting Facts
st.sidebar.header("Select Pet for Facts")
fact_pet_type = st.sidebar.selectbox(
    "Choose a pet for facts:", 
    ["-- Select --"] + facts_data["Pet Type"].tolist()
)

# Main Content for Pet Care
if pet_type != "-- Select --":
    st.subheader(f"Information for {pet_type}s")
    
    # Fetch data for the selected pet type
    pet_info = pet_data[pet_data["Pet Type"] == pet_type].iloc[0]

    # Display Pet Image
    image_url = pet_info["Image Path"]
    try:
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))
        st.image(image, caption=f"{pet_type}", use_container_width=True)
    except Exception as e:
        st.warning("Image could not be loaded. Please check the URL.")

    # Display Pet Details
    st.markdown(f"""
    *Food Name:* {pet_info["Food Name"]}  
    *Quantity:* {pet_info["Quantity"]}  
    *Feeding Time:* {pet_info["Feeding Time"]}  
    *Number of Feedings Per Day:* {pet_info["Times Per Day"]}  
    *Types of Food:* {pet_info["Types of Food"]}
    """)

else:
    st.write("Please select a pet type from the sidebar.")

# Main Content for Interesting Facts
if fact_pet_type != "-- Select --":
    st.subheader(f"Interesting Facts about {fact_pet_type}s")
    
    # Fetch facts for the selected pet
    fact_info = facts_data[facts_data["Pet Type"] == fact_pet_type].iloc[0]
    fact_image_url = fact_info["Image Path"]
    interesting_facts = fact_info["Interesting Facts"].split("|")

    # Display Pet Image for Facts
    try:
        response = requests.get(fact_image_url)
        fact_image = Image.open(BytesIO(response.content))
        st.image(fact_image, caption=f"{fact_pet_type}", use_container_width=True)
    except Exception as e:
        st.warning("Fact image could not be loaded. Please check the URL.")

    # Display Interesting Facts
    st.markdown("**Interesting Facts:**")
    for idx, fact in enumerate(interesting_facts, start=1):
        st.markdown(f"{idx}. {fact}")

# Footer
st.sidebar.info("Customize your pet care routine with this handy tool!")
