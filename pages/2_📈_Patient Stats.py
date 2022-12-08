import numpy as np
import streamlit as st
from Model import SPO2, Temperature, session, Patient, Pulse
from sqlalchemy import desc
import pandas as pd

st.set_page_config(page_title="Patient Stats", page_icon="📈")

patients_name_list = [
    (e.first_name + " " + e.last_name) for e in session.query(Patient).all()
]

st.header("Patient Stats")
st.sidebar.header("Patient Stats")

patient_name_selected = st.sidebar.selectbox("Select Patient", patients_name_list)
print(patient_name_selected)

patient_device_id = [
    patient.device_id
    for patient in session.query(Patient).filter(
        Patient.first_name + " " + Patient.last_name == patient_name_selected
    )
][0]

print("patient_device_id", patient_device_id)

st.markdown(
    """This page contains 3 sensor data of each patients.
    To look into the data of the patient, select the patient in the sidebar"""
)

st.markdown("----")
st.subheader("Latest data ({for_patient})".format(for_patient=patient_name_selected))
# st.write("Showing", patient_name_selected, "data:")

# Latest data column
col1, col2, col3 = st.columns(3)

with col1:
    try:
        curr_temp = (
            session.query(Temperature.reading)
            .filter(Temperature.from_device == patient_device_id)
            .order_by(Temperature.created_at)
        )[0]
        if curr_temp[0] is not None:
            st.markdown("# {temp} &deg;F".format(temp=curr_temp[0]))
    except:
        st.header("⚠️")
        st.write("Oops, data not available!")
    st.text("Temperature")

with col2:
    try:
        curr_pulse = (
            session.query(Pulse.reading)
            .filter(Pulse.from_device == patient_device_id)
            .order_by(Pulse.created_at)
        )[0]
        if curr_pulse[0] is not None:
            st.markdown("# {pulse} bpm".format(pulse=curr_pulse[0]))
    except:
        st.header("⚠️")
        st.write("Oops, data not available!")
    st.text("Pulse")


with col3:
    try:
        curr_spo2 = (
            session.query(SPO2.reading)
            .filter(SPO2.from_device == patient_device_id)
            .order_by(SPO2.created_at)
        )[0]
        if curr_spo2[0] is not None:
            st.markdown("# {spo2} %".format(spo2=curr_spo2[0]))
    except:
        st.header("⚠️")
        st.write("Oops, data not available!")
    st.text("SPO2")

st.markdown("----")

# summary_duration = st.sidebar.selectbox(
#     "Select duration for summary", ["1 Hour", "4 Hour", "24 Hour"]
# )
st.subheader("Summary ({for_patient})".format(for_patient=patient_name_selected))

# Summary data column
col4, col5, col6 = st.columns(3)

with col4:
    try:
        temp = [
            e.reading
            for e in session.query(Temperature).filter(
                Temperature.from_device == patient_device_id
            )
        ]
        st.markdown(
            "Min: {min_temp}&deg;F / Max: {max_temp}&deg;F".format(
                min_temp=min(temp), max_temp=max(temp)
            )
        )
        st.text("AVG: {avg}".format(avg=round(sum(temp) / len(temp), 2)))
        data = pd.DataFrame(temp, columns=["Temperature"])
        st.line_chart(data, height=200)

    except:
        st.header("⚠️")
        st.write("Oops, data not available!")

with col5:
    try:
        pulse = [
            e.reading
            for e in session.query(Pulse).filter(Pulse.from_device == patient_device_id)
        ]
        st.markdown(
            "Min: {min_pulse}bpm / Max: {max_pulse}bpm".format(
                min_pulse=min(pulse), max_pulse=max(pulse)
            )
        )
        st.text("AVG: {avg}".format(avg=round(sum(pulse) / len(pulse), 2)))
        data = pd.DataFrame(pulse, columns=["Pulse"])
        st.line_chart(data, height=200)
    except:
        st.header("⚠️")
        st.write("Oops, data not available!")

with col6:
    try:
        spo2 = [
            e.reading
            for e in session.query(SPO2).filter(SPO2.from_device == patient_device_id)
        ]
        st.markdown(
            "Min: {min_spo2}% / Max: {max_spo2}%".format(
                min_spo2=min(spo2), max_spo2=max(spo2)
            )
        )
        st.text("AVG: {avg}".format(avg=round(sum(spo2) / len(spo2), 2)))
        data = pd.DataFrame(spo2, columns=["SPO2"])
        st.line_chart(data, height=200)

    except:
        st.header("⚠️")
        st.write("Oops, data not available!")
