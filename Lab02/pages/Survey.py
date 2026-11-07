
# This creates the page for users to input data.
# The collected data is appended to data.csv.

import streamlit as st
import pandas as pd
import os

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Data Collection Survey 📝")
st.write("Please fill out the form below to add your data to the dataset.")

# DATA INPUT FORM
with st.form("survey_form"):

    # Collect the category and corresponding value
    category_input = st.text_input("Enter a category:")
    value_input = st.text_input("Enter a corresponding value:")

    submitted = st.form_submit_button("Submit Data")

    if submitted:

        # Make sure neither field is empty
        if category_input.strip() == "" or value_input.strip() == "":
            st.error("Please fill out both fields.")

        else:
            try:
                # Convert the value to a number for graphing
                numeric_value = float(value_input)

                # Create a new row
                new_data = pd.DataFrame({
                    "category": [category_input.strip()],
                    "value": [numeric_value]
                })

                # Append the row to the existing CSV file
                file_exists = os.path.exists("data.csv")
                file_is_empty = (
                    not file_exists or os.path.getsize("data.csv") == 0
                )

                new_data.to_csv(
                    "data.csv",
                    mode="a",
                    header=file_is_empty,
                    index=False
                )

                st.success("Your data has been submitted!")
                st.write(
                    f"You entered: **Category:** {category_input}, "
                    f"**Value:** {numeric_value}"
                )

            except ValueError:
                st.error("Please enter a number for the value.")

# DATA DISPLAY
st.divider()
st.header("Current Data in CSV")

# Check whether the CSV file exists and contains data
if os.path.exists("data.csv") and os.path.getsize("data.csv") > 0:

    current_data_df = pd.read_csv("data.csv")
    st.dataframe(current_data_df)

else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")
