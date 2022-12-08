import sqlalchemy as db
import streamlit as st
import time
from Model import Device, Patient, Temperature, Pulse, session
import re

available_devices = [e.id for e in session.query(Device).all() if e.vacant == 1]


st.header("Sensor Device Allotment")
with st.form("sda_form", clear_on_submit=True):
    st.write("Fill the patient details and select device.")
    first_name = st.text_input("First Name", "")
    last_name = st.text_input("Last Name", "")
    device_id = st.selectbox("Select Device ID", available_devices)

    submitted = st.form_submit_button("Allot")

    if submitted:
        while (
            re.fullmatch("[A-Za-z]{2,25}( [A-Za-z]{2,25})?", first_name)
            and not len(first_name) <= 2
            and re.fullmatch("[A-Za-z]{2,25}( [A-Za-z]{2,25})?", last_name)
            and not len(last_name) <= 2
        ):
            # code for interacting with database
            # for patient_db -> write first name, last name nad device_id
            with st.spinner("Alloting..."):
                time.sleep(1)
            try:
                session.add(
                    Patient(
                        first_name=first_name, last_name=last_name, device_id=device_id
                    )
                )
                # for device_db -> change state to alloted
                session.query(Device).filter(Device.id == device_id).update(
                    {"vacant": 0}
                )
                session.commit()
                st.success(
                    "SensorDevice ID ({device_id}) attloted to Patient {first_name}!".format(
                        device_id=device_id, first_name=first_name
                    ),
                    icon="✅",
                )
                time.sleep(3)
                st.experimental_rerun()
                break
            except Exception as e:
                session.rollback()
                session.flush()
                st.error("Something went wrong, failed to allot!", icon="🚨")
                break
        else:
            st.error(
                "First name & last name must be alphabets only. Length must be greater than 2!",
                icon="🚨",
            )
