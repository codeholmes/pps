import streamlit as st
from Model import session, Patient
import pandas as pd

st.header("Patient List")

patients = [
    [e.device_id, e.first_name, e.last_name] for e in session.query(Patient).all()
]
df = pd.DataFrame(patients)
df.rename(columns={0: "Device ID", 1: "First Name", 2: "Last Name"}, inplace=True)
st.table(df)
