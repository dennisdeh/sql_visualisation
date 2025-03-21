import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import os

DB_CONNECTION_STRING = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# Create SQLAlchemy engine
engine = create_engine(DB_CONNECTION_STRING)


# Function to get table names from the database
def fetch_tables():
    query = "SHOW TABLES"
    with engine.connect() as conn:
        tables = pd.read_sql(query, conn)
    return tables.iloc[:, 0].tolist()  # Return the first column as a list


# Function to get column names for a given table
def fetch_columns(table_name):
    query = f"SHOW COLUMNS FROM `{table_name}`"
    with engine.connect() as conn:
        columns = pd.read_sql(query, conn)
    return columns["Field"].tolist()  # Return the "Field" column as a list


# Add this function to fetch unique values of the filter column
def fetch_unique_filter_values(table_name, filter_column):
    query = f"SELECT DISTINCT `{str(filter_column)}` FROM `{table_name}`"
    with engine.connect() as conn:
        data = pd.read_sql(query, conn)
    # Return the first column as a list of unique values
    return data.iloc[:, 0].tolist()


# Function to fetch filtered data
def fetch_filtered_data(table_name, x_column, y_column, filter_column, filter_value):
    query = f"SELECT `{str(x_column)}`, `{str(y_column)}` FROM `{str(table_name)}` WHERE `{str(filter_column)}` = '{str(filter_value)}'"
    with engine.connect() as conn:
        data = pd.read_sql(query, conn)
    return data


# Streamlit UI begins here
st.title("SQL Server Data Visualizer")

# Sidebar for configuration
st.sidebar.header("Configuration")
try:
    # Step 1: Select Table
    tables = fetch_tables()
    selected_table = st.sidebar.selectbox("Select Table", tables)

    if selected_table:
        # Step 2: Select Columns
        columns = fetch_columns(selected_table)
        x_column = st.sidebar.selectbox("Select X-axis Column", columns)
        y_column = st.sidebar.selectbox("Select Y-axis Column", columns)
        filter_column = st.sidebar.selectbox("Select Filter Column", columns)

        # Step 3: Fetch unique filter values and create a dropdown for `filter_value`
        if filter_column:
            unique_values = fetch_unique_filter_values(selected_table, filter_column)
            # Add a dropdown with unique values for the filter
            filter_value = st.sidebar.selectbox(
                "Select Filter Value", unique_values, key="filter_value"
            )
        else:
            filter_value = False

        # Step 4: Fetch and visualize the data
        if st.sidebar.button("Visualize Data"):
            if all([selected_table, x_column, y_column, filter_column, filter_value]):
                try:
                    # Fetch the data
                    df = fetch_filtered_data(
                        selected_table, x_column, y_column, filter_column, filter_value
                    )

                    # Handle empty results
                    if df.empty:
                        st.warning("No data found for the specified filter.")
                    else:
                        # Sort
                        df = df.sort_values(by=x_column, ascending=True)
                        # Display the data in a table
                        st.dataframe(df)

                        # Visualize the data with Plotly
                        fig = px.line(
                            df,
                            x=x_column,
                            y=y_column,
                            title=f"{y_column} vs {x_column} (Filtered by {filter_column} = {filter_value})",
                        )
                        st.plotly_chart(fig)
                except Exception as e:
                    st.error(f"Error fetching data: {e}")
            else:
                st.warning("Please fill in all the necessary fields.")
except Exception as e:
    st.error(f"Error connecting to the database: {e}")
