import streamlit as st
import time
import pandas as pd
import joblib
import random
import pymongo

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["streamlit_data"]
collection = db["data"]

data_list = []

def inference(process,cpu_usage,ram_usage):
    clf = joblib.load("anomaly_model.pkl")

    data = pd.DataFrame({'max_cpu_usage': [cpu_usage],
                     'max_ram_usage': [ram_usage]})

    prediction = clf.predict(data)
    return prediction[0]

def generate_random_values():
    processes = ["Search", "Service Host", "Runtime Service", "Application", "Sync Service", "Network Host", "Client Server", "Container", "Train"]
    process = random.choice(processes)
    cpu_usage = random.randint(0, 100)
    ram_usage = random.randint(0, 100)
    return process, cpu_usage, ram_usage

def form():  
    col1, col2 = st.columns([2, 1])

    # Form for manual entry
    with col1:
        st.subheader("Manual Check")  
        form = st.form("Manual Entry", clear_on_submit=True, border=True)
        process1 = form.selectbox(label="Select the System Process", options=("Search","Service Host","Runtime Service", "Application", "Sync Service", "Network Host", "Client Server", "Container", "Train"))
        cpu = form.number_input("CPU Usage (%)",step=0.1,value=0.1)
        memory = form.number_input("Memory Usage (MB)", step=1,value=1)
        submitted = form.form_submit_button("Submit")
        if submitted:
            st.success('Form submitted successfully!')
            with st.spinner(text="Generating the result"):
             time.sleep(1)
             result1 = inference(process=process1, cpu_usage=cpu, ram_usage=memory)   
             data_list.append({"Name": process1, "CPU Usage": cpu, "Memory Usage": memory, "Behaviour":result1}) 
             st.info(f"The behavior of process '{process1}' is predicted to be: {result1}")

    # Button for random data check
    with col2:
        st.subheader("Random Process Check")
        if st.button("Check with random data"):
            st.success("Data Sucessfully Generated")
            process2, cpu_usage, ram_usage = generate_random_values()
            with st.spinner(text="Generating the result"):
                time.sleep(1)
                result2 = inference(process=process2, cpu_usage=cpu_usage, ram_usage=ram_usage)  
                data_list.append({"Name": process2, "CPU Usage": cpu_usage, "Memory Usage": ram_usage,"Behaviour":result2})  
                st.info(f"The behavior of process '{process2}' is predicted to be: {result2}")

    # Display output dataframe below
    if data_list:
        st.subheader("Output")
        for data in data_list:
            try:
                collection.insert_one(data)
            except :
                  a = 10
        df = pd.DataFrame(data_list)
        st.table(df)          
        clear_list = st.button("Clear List", type='primary')
        if clear_list:
            data_list.clear()
            st.rerun()
