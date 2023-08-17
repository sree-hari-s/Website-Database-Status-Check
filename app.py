import requests
import pyodbc
import streamlit as st

website_url = [
    #List of website URLs

]

statuses = {
    200: "Website Available",
    301: "Permanent Redirect",
    302: "Temporary Redirect",
    404: "Not Found",
    500: "Internal Server Error",
    503: "Service Unavailable",
    403: "Forbidden response",
    522: "Connection Timeout Error",
    530: "The site is frozen",
    5031: "Under Maintenance"  # Added status code and message for maintenance page
}

status_counts = {status: 0 for status in statuses.values()}
status_counts['Request Exception'] = 0  # Initialize count for 'Request Exception'

st.title("Website Status")

for index, url in enumerate(website_url, start=1):
    try:
        web_response = requests.get(url)
        status_code = web_response.status_code
        status = statuses.get(status_code, "Unknown Status")

        if "under maintenance" in web_response.text.lower():
            status = statuses[5031]  # Set status to "Under Maintenance" if maintenance page is detected

        status_counts[status] += 1
        st.write(f"{index}. {url}: {status}")
        
    except requests.exceptions.ConnectionError:
        status = "Request Exception"
        status_counts[status] += 1
        st.write(f"{index}. {url}: {status}")

# List of database connection settings
databases = [
    # Add more databases here
    # {
    #     'server': 'sql5053.site4now.net',
    #     'database': 'db_a3864d_tlhr',
    #     'username': 'db_a3864d_tlhr_admin',
    #     'password': 'TL@05tsAS2020'
    # },
    
]

# Streamlit app
st.title("Database Statistics")

total_databases = len(databases)

for db in databases:
    try:
        # Establish the connection
        conn = pyodbc.connect(
            f'DRIVER=ODBC Driver 17 for SQL Server;'
            f'SERVER={db["server"]};'
            f'DATABASE={db["database"]};'
            f'UID={db["username"]};'
            f'PWD={db["password"]};'
        )

        # Define the stored procedure call
        procedure_call = f"EXEC GetTableAndSPCounts"

        # Create a cursor
        cursor = conn.cursor()

        # Execute the stored procedure
        cursor.execute(procedure_call)

        # Fetch the results
        results = cursor.fetchall()

        # Close the cursor
        cursor.close()

        # Close the connection
        conn.close()

        # Display results
        st.subheader(f"Database: {db['database']}")
        if len(results) == 0:
            st.write("No results to display.")
        else:
            for row in results:
                st.write(f"Tables: {row.Table_Count}, Stored Procedures: {row.SP_Count}")

    except pyodbc.Error as ex:
        st.error(f"An error occurred for {db['database']}: {ex}")

st.title("Website Status Counts")

for status, count in status_counts.items():
    st.write(f"{status}: {count}")

st.title("Website Status Counts (Statuses with Count > 0)")

for status, count in status_counts.items():
    if count > 0:
        st.write(f"{status}: {count}")
st.title(f"Total number of databases: {total_databases}")