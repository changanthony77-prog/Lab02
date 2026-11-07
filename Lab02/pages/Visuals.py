
# This creates the page for displaying data visualizations.

import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
from pathlib import Path


# ==========================================
# FILE PATHS
# ==========================================

# Locate the main GitHub repository folder.
PROJECT_DIR = Path(__file__).resolve().parents[2]

JSON_PATH = PROJECT_DIR / "data.json"
CSV_PATH = PROJECT_DIR / "data.csv"


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Data Visualizations",
    page_icon="📈",
    layout="wide"
)


# ==========================================
# PAGE TITLE
# ==========================================

st.title("Data Visualizations 📈")


# ==========================================
# PART 1: GRAPHS FROM data.json
# ==========================================

st.header("Part 1: South Korea's Tallest Buildings")

st.write(
    "Explore the heights and completion years of some of "
    "South Korea's tallest buildings."
)


# Read the JSON file.

if JSON_PATH.exists():

    with open(JSON_PATH, "r") as file:
        data = json.load(file)

    data_points = data["data_points"]


    # --------------------------------------
    # GRAPH 1: STATIC BAR CHART
    # --------------------------------------

    st.subheader("1. Comparing Building Heights")

    st.write(
        "This chart compares the heights of all five buildings "
        "in the dataset."
    )

    building_names = []
    building_heights = []

    for building in data_points:
        building_names.append(building["label"])
        building_heights.append(building["value"])

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.bar(building_names, building_heights)

    ax.set_title(data["chart_title"])
    ax.set_xlabel("Building")
    ax.set_ylabel("Height (meters)")

    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)


    # --------------------------------------
    # GRAPH 2: DYNAMIC SCATTER PLOT
    # --------------------------------------

    st.subheader("2. Explore Building Heights")

    st.write(
        "Select a year and a building to explore the data."
    )

    if "year_cutoff" not in st.session_state:
        st.session_state.year_cutoff = 2011

    st.slider(
        "Show buildings completed in or after:",
        min_value=2011,
        max_value=2020,
        key="year_cutoff"
    )

    # Filter buildings by year.

    selected_buildings = []

    for building in data_points:

        if building["year_built"] >= st.session_state.year_cutoff:
            selected_buildings.append(building)

    # Sort buildings from oldest to newest.

    selected_buildings.sort(
        key=lambda building: building["year_built"]
    )

    if len(selected_buildings) > 0:

        building_names = []

        for building in selected_buildings:
            building_names.append(building["label"])

        selected_building_name = st.selectbox(
            "Choose a building to highlight:",
            building_names
        )

        selected_years = []
        selected_heights = []

        for building in selected_buildings:
            selected_years.append(building["year_built"])
            selected_heights.append(building["value"])

        fig2, ax2 = plt.subplots(figsize=(10, 5))

        ax2.scatter(
            selected_years,
            selected_heights,
            label="Other buildings"
        )

        # Highlight selected building.

        for building in selected_buildings:

            if building["label"] == selected_building_name:

                ax2.scatter(
                    building["year_built"],
                    building["value"],
                    s=180,
                    marker="*",
                    label="Selected building"
                )

                ax2.annotate(
                    building["label"],
                    (building["year_built"], building["value"]),
                    xytext=(8, 8),
                    textcoords="offset points",
                    fontsize=9
                )

        ax2.set_title("Building Height by Completion Year")
        ax2.set_xlabel("Year Completed")
        ax2.set_ylabel("Height (meters)")

        ax2.set_xticks(sorted(set(selected_years)))

        ax2.legend()
        plt.tight_layout()

        st.pyplot(fig2)
        plt.close(fig2)

    else:

        st.warning("No buildings match the selected year.")

else:

    st.error(
        "data.json could not be found. "
        "Check that it is uploaded to the main GitHub repository."
    )


# ==========================================
# PART 2: GRAPHS FROM data.csv
# ==========================================

st.divider()

st.header("Part 2: Survey Data")

st.write(
    "Explore the categories and values submitted through "
    "the Data Collection Survey."
)


# Check whether data.csv exists.

if CSV_PATH.exists() and CSV_PATH.stat().st_size > 0:

    survey_df = pd.read_csv(CSV_PATH)

    # Standardize column names.

    survey_df.columns = (
        survey_df.columns.str.strip().str.lower()
    )

    st.subheader("Submitted Survey Responses")

    st.dataframe(survey_df)

    # Check required columns.

    if "category" in survey_df.columns and "value" in survey_df.columns:

        survey_df["value"] = pd.to_numeric(
            survey_df["value"],
            errors="coerce"
        )

        survey_df = survey_df.dropna(
            subset=["category", "value"]
        )

        if not survey_df.empty:

            # Calculate category totals.

            category_totals = survey_df.groupby(
                "category"
            )["value"].sum()

            category_totals = category_totals.sort_values(
                ascending=False
            )


            # --------------------------------------
            # GRAPH 3: STATIC BAR CHART
            # --------------------------------------

            st.subheader("3. Total Values by Category")

            st.write(
                "This bar chart compares the total values "
                "submitted for each category."
            )

            fig3, ax3 = plt.subplots(figsize=(10, 5))

            ax3.bar(
                category_totals.index,
                category_totals.values
            )

            ax3.set_title("Total Values for Each Category")
            ax3.set_xlabel("Category")
            ax3.set_ylabel("Total Value")

            plt.xticks(rotation=35, ha="right")
            plt.tight_layout()

            st.pyplot(fig3)
            plt.close(fig3)


            # --------------------------------------
            # GRAPH 4: DYNAMIC PIE CHART
            # --------------------------------------

            st.subheader("4. Explore Survey Categories")

            st.write(
                "Use the slider to choose how many of the largest "
                "categories appear individually in the pie chart."
            )

            max_categories = len(category_totals)

            if "number_of_categories" not in st.session_state:
                st.session_state.number_of_categories = min(
                    3, max_categories
                )

            st.session_state.number_of_categories = min(
                st.session_state.number_of_categories,
                max_categories
            )

            # Category selection slider.

            if max_categories > 1:

                st.slider(
                    "Number of categories to display:",
                    min_value=1,
                    max_value=max_categories,
                    key="number_of_categories"
                )

            else:

                st.write("Only one category is available.")

            number_selected = st.session_state.number_of_categories

            # Get largest categories.

            top_categories = category_totals.head(
                number_selected
            )

            # Get remaining categories.

            remaining_categories = category_totals.iloc[
                number_selected:
            ]

            pie_labels = list(top_categories.index)
            pie_values = list(top_categories.values)

            # Combine remaining categories into Other.

            if len(remaining_categories) > 0:

                pie_labels.append("Other")
                pie_values.append(remaining_categories.sum())

            # Create pie chart.

            fig4, ax4 = plt.subplots(figsize=(8, 6))

            ax4.pie(
                pie_values,
                labels=pie_labels,
                autopct="%1.1f%%",
                startangle=90
            )

            ax4.set_title("Distribution of Survey Values")

            plt.tight_layout()

            st.pyplot(fig4)
            plt.close(fig4)

        else:

            st.warning("No valid survey data is available.")

    else:

        st.warning(
            "Your data.csv file must contain Category and Value columns."
        )

else:

    st.warning("No survey data has been submitted yet.")
