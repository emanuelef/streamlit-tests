import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

st.title('Flightpaths')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://now-mongo-api-mudhdoba1-emanuelef.vercel.app/api/'
            'allFlights.js?start=1566317600&end=1566361999&interpolation=1')

@st.cache
def load_data():
    data = pd.read_json(DATA_URL)
    data["startTime"] = pd.to_datetime(data["startTime"], unit='s')
    return data

data_load_state = st.text('Loading data...')
data = load_data().dropna()
data_load_state.text("Done! (using st.cache)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of flights by hour')
hist_values = np.histogram(data["startTime"].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

number = st.number_input('Enter a number', value=0, min_value=0, max_value=len(data)-1)

df_test = pd.DataFrame.from_records(data.iloc[number]['positions'],
 columns=['lat', 'lon', 'alt', 'time'])
st.write(df_test)

st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=51.4777,
        longitude=-0.4802,
        zoom=10,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
           'HexagonLayer',
           data=df_test,
           get_position='[lon, lat]',
           radius=200,
           elevation_scale=4,
           elevation_range=[0, 1000],
           pickable=True,
           extruded=True,
        ),
    ],
))