from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import plotly.express as px
import pymongo
import plotly.graph_objs as go

st.set_page_config(page_title="TGR_39",
                    page_icon="🧊",
                    layout="wide")


MONGO_DETAILS = "mongodb://tesarally:contestor@mongodb:27017"

@st.cache_resource
def init_connection():
    return pymongo.MongoClient(MONGO_DETAILS)

client = init_connection()

@st.cache_data(ttl=0)
def get_data():
    db = client.Waterlevel
    items = db.water_height.find()
    items = list(items)
    return items

def reload_data():
    global items, df
    items = get_data()
    df = pd.DataFrame(items)
    
items = get_data()


df = pd.DataFrame(items)

st.markdown(
    "<h1 style='text-align: center; color: white; "
    "background-color: #145DA0; padding: 10px;'>Water Height Database</h1>",
    unsafe_allow_html=True
)

st.write(" ")

if st.button("Refresh Data"):
        reload_data()


df_st = df[df['date'] != 0]
df_st = df_st.drop(columns=['_id','w_height'])
df_st = df_st.to_records(index=False)
last_measure = df.tail(1)['w_height'].max()

#SideBar
col1, col2, col3 = st.columns(3)
st.sidebar.header("Please Filter Here:")
page_type = st.sidebar.selectbox("Select type :",
        options = ["Table","Graphs", "Charts", "Metrics"],
)

if page_type == "Table" :
        st.markdown("<p style='color: #94F0FF; padding: 5px; font-size: 40px;'>Water Database</p>", unsafe_allow_html=True)
        st.table(df_st)

if page_type == "Graphs" :
        fig_w_Q3 = px.line(df_st, x='date', y='w_H3', title='Water_H3')
        fig_w_H3 = px.line(df_st, x='date', y='w_Q3', title='Water_Q3')
        st.plotly_chart(fig_w_Q3)
        st.plotly_chart(fig_w_H3)
        
        fig = px.scatter(df, x='w_H3', y='w_Q3', labels={'w_H3': 'w_H3', 'w_Q3': 'w_Q3'}, title='Scatter Plot: Correlation between Water_H3 and Water_Q3')
        st.plotly_chart(fig)


if page_type == "Charts" :
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df_st['date'], y=df_st['w_H3'], name='Water_H3'))
        fig.add_trace(go.Bar(x=df_st['date'], y=df_st['w_Q3'], name='Water_Q3'))
        fig.update_layout(barmode='group', xaxis_title='Date', yaxis_title='Height Level', title='Comparison of Water Levels')
        st.plotly_chart(fig)
    
if page_type == "Metrics" :
        mean_values2 = df_st['w_H3'].mean()
        max_values2 = df_st['w_H3'].max()
        min_values2 = df_st['w_H3'].min()
        mean_values3 = df_st['w_Q3'].mean()
        max_values3 = df_st['w_Q3'].max()
        min_values3 = df_st['w_Q3'].min()
        
        col1, col2 = st.columns(2)
        
        with col1:
                st.metric(label="Water H3 Mean", value=mean_values2)
                st.metric(label="Water H3 Max", value=max_values2)
                st.metric(label="Water H3 Min", value=min_values2)
        with col2:
                st.metric(label="Water Q3 Mean", value=mean_values3)
                st.metric(label="Water Q3 Max", value=max_values3)
                st.metric(label="Water Q3 Min", value=min_values3)


