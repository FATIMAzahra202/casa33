import streamlit as st  # Importing the Streamlit module
import pandas as pd  # Importing the Pandas module for working with dataframes
import os  # Importing the os module for interacting with system files and directories
import matplotlib.pyplot as plt  # Importing Matplotlib for plotting

# Path to the CSV file containing city data
csv_file_path = 'city_data.csv'

def load_data():
    # Check if the file exists and is not empty
    if os.path.exists(csv_file_path) and os.stat(csv_file_path).st_size > 0:
        # If it exists, load the data from the CSV file
        return pd.read_csv(csv_file_path)
    else:
        # If it doesn't exist, create new default data
        data = {
            "City": ["Casablanca", "Rabat", "Marrakech", "Fez", "Tangier"],
            "Population": [3369000, 577827, 928850, 1112072, 947952],
            "Area (km²)": [220, 118, 230, 320, 144]
        }
        df = pd.DataFrame(data)
        save_data(df)  # Save the default data to a new CSV file
        return df

def save_data(df):
    # Save DataFrame to CSV file without including the index
    df.to_csv(csv_file_path, index=False)

def add_city(df):
    # Create a form to add a new city to the database
    with st.form("add_city_form"):
        new_city = st.text_input("City name")
        new_population = st.number_input("Population", min_value=0, step=1000, format="%d")
        new_area = st.number_input("Area (km²)", min_value=0, step=1, format="%d")
        submitted = st.form_submit_button("Add City")
        if submitted:
            # If the submission is successful, add the new city to the dataframe
            if new_city and new_population and new_area:
                new_data = pd.DataFrame({'City': [new_city], 'Population': [new_population], 'Area (km²)': [new_area]})
                df = pd.concat([df, new_data], ignore_index=True)
                save_data(df)  # Save the updated DataFrame to CSV
                st.success(f"Added {new_city} to the database.")
            else:
                st.error("Please fill out all fields to add a new city.")
    return df

def display_statistics(df):
    st.title('Moroccan Cities Statistics')  # Title of the page
    st.write("Here are some statistics about major cities in Morocco:")  # Description of the page
    st.dataframe(df)  # Display the DataFrame on the page
    
    # Create a bar chart using Matplotlib
    plt.figure(figsize=(10, 6))
    plt.bar(df["City"], df["Population"], color='skyblue')
    plt.xlabel("City")
    plt.ylabel("Population")
    plt.title("Population of Major Moroccan Cities")
    plt.xticks(rotation=45, ha='right')
    st.pyplot()  # Display the plot on the page

    # Add a download button to download the data as a CSV file
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='city_data.csv',
        mime='text/csv',
    )

def main():
    df = load_data()  # Load the data
    df = add_city(df)  # Add cities
    display_statistics(df)  # Display the statistics

if __name__ == "__main__":
    st.set_page_config(page_title='Moroccan Cities Data', layout='wide')  # Configure the page
    main()  # Run the application
