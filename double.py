import streamlit as st
import pandas as pd
import sqlite3


# Function to fetch unique values for the first dropdown
def fetch_first_dropdown_options():
    conn = sqlite3.connect('database.db')  # Update with your database path
    query = 'SELECT DISTINCT प्रमण्डल FROM your_table_name;'  # Update with your column and table
    df = pd.read_sql_query(query, conn)
    conn.close()
    options = ['Select'] + df['प्रमण्डल'].dropna().unique().tolist()
    return options


# Function to fetch related values for the second dropdown based on selection from the first dropdown
def fetch_second_dropdown_options(selected_value):
    conn = sqlite3.connect('database.db')  # Update with your database path
    query = "SELECT DISTINCT जिला FROM your_table_name WHERE प्रमण्डल = ?;"  # Use parameterized query
    df = pd.read_sql_query(query, conn, params=(selected_value,))
    conn.close()
    options = ['Select'] + df['जिला'].dropna().unique().tolist()
    return options


# Streamlit app
st.set_page_config(page_title="Khel Vyamshala", layout="wide")

# Sidebar for navigation
st.sidebar.header("Navigation")
st.sidebar.write("Select an option from the dropdowns to view data.")

# Title and description
st.title('Khel Vyamshala')
st.markdown("""
    Welcome to the **Khel Vyamshala** Database Portal! Use the dropdown menus below to select a division and district.
""")

# Add some space between elements
st.write("<br>", unsafe_allow_html=True)

# First dropdown
first_dropdown_options = fetch_first_dropdown_options()
selected_first_option = st.selectbox(
    'Select Division:', first_dropdown_options,
    index=0,
    help="Choose a division from the list to populate the districts dropdown."
)

# Initialize second dropdown
second_dropdown_options = []
selected_second_option = None

# Second dropdown (conditional on the first dropdown selection)
if selected_first_option and selected_first_option != 'Select':
    second_dropdown_options = fetch_second_dropdown_options(selected_first_option)
    selected_second_option = st.selectbox(
        'Select District:', second_dropdown_options,
        index=0,
        help="Choose a district based on the selected division."
    )

# Add some space before displaying results
st.write("<br>", unsafe_allow_html=True)

# Final query based on both dropdown selections
if selected_first_option != 'Select' and selected_second_option != 'Select':
    conn = sqlite3.connect('database.db')  # Update with your database path
    query = "SELECT * FROM your_table_name WHERE प्रमण्डल = ? AND जिला = ?;"

    try:
        df = pd.read_sql_query(query, conn, params=(selected_first_option, selected_second_option))
        st.write(df)
    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        conn.close()
else:
    st.write("Please select valid options from both dropdowns to view the data.")

# Add a footer
st.markdown("""
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background-color: #f1f1f1;
            text-align: center;
            padding: 10px;
            color: #888;
            font-size: 12px;
        }
    </style>
    <div class="footer">
        <p>© 2024 Khel Vyamshala. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)
