import streamlit as st
import numpy as np
import pandas as pd
from Model import session, Patient, Pulse, Temperature, SPO2, Device

sensor_proxy = st.sidebar.selectbox("Select Sensor", ["Temperature", "Pulse", "SPO2"])

st.header("CompareData")

st.markdown(
    """This page contains sensor-wise chart for comparing patient's condition.
    \nIn the sidebar, select Sensor type and chart to see plot!"""
)


sensor = Temperature
if sensor_proxy == "Pulse":
    sensor = Pulse
elif sensor_proxy == "SPO2":
    sensor = SPO2


chart_type = st.sidebar.selectbox(
    "Select Chart", ["Line Chart (Raw Data)", "Bar Graph (Average Data)"]
)

# fetch data point from the db

# db query for device
devices = [e.from_device for e in session.query(sensor).all()]

# db query for data
data = {e: [] for e in devices}
data_list = []
for k, v in data.items():
    data[k] = [e.reading for e in session.query(sensor).filter(sensor.from_device == k)]
    data_list.append(data[k])
# print(data_list)

# db query for data point
min_value = len(data_list[0]) - (len(data_list[0]))
max_value = len(data_list[0]) - 1
start_data_point, end_data_point = st.sidebar.select_slider(
    "Data Point",
    options=[str(e) for e in range(len(data_list[0]))],
    value=(str(min_value), str(max_value)),
)

patients = {
    e.device_id: e.first_name + " " + e.last_name for e in session.query(Patient).all()
}
print(patients)
# print(pd.DataFrame(data))
if chart_type == "Line Chart (Raw Data)":
    filtered_data = {
        k: v[int(start_data_point) : int(end_data_point) + 1] for k, v in data.items()
    }
    named_data = {}
    for k, v in filtered_data.items():
        for id, name in patients.items():
            if k == id:
                named_data.update({name: v})
    # print(named_data)
    st.text("Chart (Raw data)")
    st.line_chart(pd.DataFrame(named_data, index=None), x="")
elif chart_type == "Bar Graph (Average Data)":
    filtered_data = {
        k: v[int(start_data_point) : int(end_data_point)] for k, v in data.items()
    }
    # filtered_data: {"device_id":[data]}
    # convert the data into below structure
    # structure: {"name":[], "avg":[]}
    devices_list = [k for k, v in filtered_data.items()]
    data_list = [round(sum(v) / len(v), 2) for k, v in filtered_data.items()]
    filtered_data_2 = {
        "device_id": [k for k, v in filtered_data.items()],
        "avg": [round(sum(v) / len(v), 2) for k, v in filtered_data.items()],
    }
    # print(filtered_data_2)

    # replacing id with name
    filtered_data_3 = {}
    p_names = []
    for k, v in filtered_data_2.items():
        if k == "device_id":
            for e in v:
                p_names.append(patients[e])
    # print(p_names)

    filtered_data_3 = {
        "Patient Name": p_names,
        "Avg. {}".format(sensor_proxy): [
            round(sum(v) / len(v), 2) for k, v in filtered_data.items()
        ],
    }

    st.text("Bar Graph (Average Data)")
    st.bar_chart(pd.DataFrame(filtered_data_3).set_index("Patient Name"), height=600)

    # st.markdown("### Prioritised List")
    # st.text("Patients which needs to visit according to SPO2 reading:")
    # prioritised_list = []
    # p_name_avg = []
    # p_avg = []
    # spo2_reading = []
    # for k, v in filtered_data_3.items():
    #     if k == "Patient Name":
    #         for e in v:
    #             p_name_avg.append((p_name_avg))
    #         pass
    #     if k == "Avg. SPO2":
    #         p_avg.append(v)
    #         avg_list = v.copy()
    #         avg_list.sort()
    #         spo2_reading = avg_list.copy()
    #         print(avg_list)

    # {p_name: avg}
    # for k, v in filtered_data_3.items():
    #     if k == "Patient Name":
    #         for e in spo2_reading:
    #             if
    #         pass
