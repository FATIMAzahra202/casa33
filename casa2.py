import streamlit as st  
import pandas as pd  
import os 

csv_file_path = 'city_data.csv'

def load_data():
    if os.path.exists(csv_file_path) and os.stat(csv_file_path).st_size > 0:
        return pd.read_csv(csv_file_path)
    else:
        data = {
            "City": ["Casablanca", "Rabat", "Marrakech", "Fez", "Tangier"],
            "Population": [3369000, 577827, 928850, 1112072, 947952],
            "Area (km²)": [220, 118, 230, 320, 144]
        }
        df = pd.DataFrame(data)
        save_data(df)
        return df

def save_data(df):
    df.to_csv(csv_file_path, index=False)

def add_city(df):
    with st.form("add_city_form"):
        new_city = st.text_input("City name")
        new_population = st.number_input("Population", min_value=0, step=1000, format="%d")
        new_area = st.number_input("Area (km²)", min_value=0, step=1, format="%d")
        submitted = st.form_submit_button("Add City")
        if submitted:
            if new_city and new_population and new_area:
                new_data = pd.DataFrame({'City': [new_city], 'Population': [new_population], 'Area (km²)': [new_area]})
                df = pd.concat([df, new_data], ignore_index=True)
                save_data(df)
                st.success(f"Added {new_city} to the database.")
            else:
                st.error("Please fill out all fields to add a new city.")
    return df

def display_statistics(df):
    st.title('Moroccan Cities Statistics')  
    st.write("Here are some statistics about major cities in Morocco:")  
    st.dataframe(df)  
    
    # Using Matplotlib for plotting
    try:
        import matplotlib.pyplot as plt  
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(df["City"], df["Population"], color='skyblue')
        ax.set_xlabel("City")
        ax.set_ylabel("Population")
        ax.set_title("Population of Major Moroccan Cities")
        ax.tick_params(axis='x', rotation=45, ha='right')
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error plotting data: {e}")

    # Download button
    try:
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='city_data.csv',
            mime='text/csv',
        )
    except Exception as e:
        st.error(f"Error generating download button: {e}")

def main():
    try:
        df = load_data()  
        df = add_city(df)  
        display_statistics(df)  
    except Exception as e:
        st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    st.set_page_config(page_title='Moroccan Cities Data', layout='wide')  
    main()  
