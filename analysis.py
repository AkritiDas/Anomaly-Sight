import streamlit as st
import pandas as pd
import pymongo
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to MongoDB
try:
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["streamlit_data"]
    collection = db["data"]
    is_connected = True
except pymongo.errors.ConnectionFailure:
    is_connected = False

def fetch_data():
    cursor = collection.find({})
    data = list(cursor)
    df = pd.DataFrame(data)
    return df

# Define function to clear MongoDB collection
def clear_mongodb():
    collection.delete_many({})
    st.success("MongoDB collection cleared successfully!")

def dash():
    if is_connected and "data" in db.list_collection_names():
        # Fetch data from MongoDB
        cursor = collection.find({})
        mongo_data = list(cursor)

        # Display the data in a DataFramex
        if mongo_data:
            st.subheader("Data from Mongo Database")
            df = pd.DataFrame(mongo_data)
            st.table(df)
            if st.button("Clear MongoDB Collection",type='primary'):
                clear_mongodb()
                st.rerun()
        else:
            st.write("No data available in Mongo DataBase.")
    
    else:
        st.write("Failed to connect to MongoDB or the collection does not exist.")

def plot_data():
    # Streamlit app
    st.title("Data Visualization from MongoDB")

    # Fetch data from MongoDB
    df = fetch_data()  
    df = df.iloc[:, 1:]

    # Select columns for plotting
    st.sidebar.subheader("Select Columns")
    x_axis = st.sidebar.selectbox("X-axis", df.columns)
    y_axis = st.sidebar.selectbox("Y-axis", df.columns)

    # Select plot type
    plot_type = st.sidebar.selectbox("Select Plot Type", ["Bar Plot", "Box Plot", "Histogram", "Scatter Plot", "Line Plot"])
    try:
        # Check if the specified columns are None
        if x_axis is None or y_axis is None:
            st.error("Please select valid columns for plotting.")
            return
    except KeyError:
        st.error("One or more specified columns does not exist in the DataFrame.")
    # Plot the selected data
    if plot_type == "Bar Plot":
        st.subheader("Bar Plot")
        fig, ax = plt.subplots()
        ax.bar(df[x_axis], df[y_axis])
        ax.set_xlabel(x_axis)
        ax.set_ylabel(y_axis)
        ax.set_title("Bar Plot")
        st.pyplot(fig)

    elif plot_type == "Box Plot":
        if not pd.api.types.is_numeric_dtype(df[x_axis]) or not pd.api.types.is_numeric_dtype(df[y_axis]):
            st.error("Column should be numeric for box plotting.")
            return

        # Create the plot
        st.subheader("Box Plot")
        fig, ax = plt.subplots()
        sns.boxplot(x=df[x_axis], y=df[y_axis], ax=ax)
        st.pyplot(fig)

    elif plot_type == "Histogram":
        st.subheader("Histogram")
        fig, ax = plt.subplots()
        ax.hist(df[y_axis])
        ax.set_xlabel(y_axis)
        ax.set_ylabel("Frequency")
        ax.set_title("Histogram")
        st.pyplot(fig)

    elif plot_type == "Scatter Plot":
        st.subheader("Scatter Plot")
        fig, ax = plt.subplots()
        ax.scatter(df[x_axis], df[y_axis])
        ax.set_xlabel(x_axis)
        ax.set_ylabel(y_axis)
        ax.set_title("Scatter Plot")
        st.pyplot(fig)

    elif plot_type == "Line Plot":
        st.subheader("Line Plot")
        fig, ax = plt.subplots()
        ax.plot(df[x_axis], df[y_axis])
        ax.set_xlabel(x_axis)
        ax.set_ylabel(y_axis)
        ax.set_title("Line Plot")
        st.pyplot(fig)
