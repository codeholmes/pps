import streamlit as st
import pandas as pd
import time
from Model import Device, session

st.header("Add SensorDevice")

st.text("Currently Available Sensor Device (Both alloted or not alloted!)")
available_devices = [
    [e.id, e.device_name, e.vacant] for e in session.query(Device).all()
]
df = pd.DataFrame(available_devices)
df.rename(columns={0: "Device ID", 1: "Device Name", 2: "Vacant"}, inplace=True)
print(df)
st.table(df)

with st.form("add_sd_form", clear_on_submit=True):
    device_name = st.text_input("Enter SensorDevice name: ")
    submitted = st.form_submit_button("Add")
    if submitted:
        with st.spinner("Adding..."):
            time.sleep(2)
        try:
            session.add(Device(device_name=device_name, vacant=True))
            session.commit()
            st.success(
                "SensorDevice ({sd_name}) added!".format(sd_name=device_name), icon="✅"
            )
            time.sleep(3)
            st.experimental_rerun()
        except Exception as e:
            session.rollback()
            session.flush()
            st.error("Something went wrong, failed to add!", icon="🚨")
