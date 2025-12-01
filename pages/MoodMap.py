import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from transformers import pipeline
from datetime import datetime as dt,time
import pytz
import os

#Load emotion model (cached) so it doesn't reload every run
@st.cache_resource
def load_model():
    return pipeline(
        "text-classification",
        model="j-hartmann/emotion-english-distilroberta-base", 
        return_all_scores=True
    )

classifier = load_model()

if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=[
        "Timestamp", "Text", "Compound Score", "Positive", "Neutral", "Negative"
    ])

st.subheader("🫧 My Mood Map")

tf_choice = st.selectbox("Timeframe", ["Today", "This Week", "This Month", 
                           "This Year", "Custom Dates"])
log_path = "mood_logs.csv"
if ("data" in st.session_state and not st.session_state.data.empty)\
        or (os.path.exists(log_path)):
    if os.path.exists(log_path):
        log_data = pd.DataFrame(pd.read_csv(log_path))
    else:
        log_data = st.session_state.data
    
    local_tz = pytz.timezone("America/Los_Angeles")
    curr_day = dt.now(local_tz).date()
    curr_week = dt.now().isocalendar().week
    curr_month = dt.now().month
    curr_year = dt.now().year
    log_data["Timestamp"] = pd.to_datetime(log_data["Timestamp"], 
                                                   errors="coerce")
    if tf_choice=="Today":
        log_data = log_data[log_data["Timestamp"].dt.date 
                               == curr_day]
    elif tf_choice == "This Week":
        log_data = log_data[log_data["Timestamp"].dt.isocalendar().week
                            == curr_week]
    elif tf_choice == "This Month":
        log_data = log_data[log_data["Timestamp"].dt.month
                            == curr_month]
    elif tf_choice == "This Year":
        log_data = log_data[log_data["Timestamp"].dt.year
                            == curr_year]
    else:
        custom_range = st.date_input("Select a date range",
                                        value=(dt.now().date(), 
                                        dt.now().date()))
        if len(custom_range) == 2:
            start_date = custom_range[0]
            end_date = custom_range[1]
        else:
            st.warning("Please select both a start date and an end dates!")
            st.stop()
        start_datetime = dt.combine(start_date, time.min).replace(tzinfo=local_tz)
        end_datetime = dt.combine(end_date, time.max).replace(tzinfo=local_tz)
            
        log_data = log_data[(log_data["Timestamp"] >= start_datetime) &
                               (log_data["Timestamp"] <= end_datetime)]
        
    if log_data.shape[0] == 0:
        st.warning("No mood logs found yet!")
        

    else:    
        text_data = log_data["Text"].dropna().astype(str).tolist()

        #Run classifier on each entry
        all_results = []
        
        for entry in text_data:
            res = classifier(entry)[0] #return a list of dicts like: [{"label": "joy", "score": 0.5},
                                        #                           {"label": "fear", "score":0.75}...]
            results = {r["label"]:r["score"] for r in res} #flat dict: {"joy":0.25,"fear":0.75}
            results["Entry"] = entry #adds a new key "Text" to the flat dict with the actual text entry
            all_results.append(results)        

        df = pd.DataFrame(all_results)

        emotion_cols = [c for c in df.columns if c != "Entry"]
        heatmap_data = df[emotion_cols].T  # transpose so emotions are on y-axis

        colorscale = [
        [0.0, '#fde9c4'],    # Very light gold
        [0.16, '#f9d7a7'],   # Light gold
        [0.32, '#f5c285'],   # Medium gold-orange
        [0.48, '#e8a761'],   # Muted orange
        [0.64, '#c97c5c'],   # Soft reddish-brown
        [0.8, '#9c4f46'],    # Darker red-brown
        [1.0, '#622c25']     # Deep brown
    ]

    # Create heatmap
        fig = px.imshow(
            heatmap_data,
            labels=dict(x="Entry", y="Emotion", color="Score"),
            x=[f"Entry {i}" for i in df['Entry']],
            y=emotion_cols,
            color_continuous_scale=colorscale
        )
        fig.update_layout(
        width=1000,   # fixed width that fits your app
        height=800,
        xaxis=dict(visible=False),
        yaxis=dict(title="Emotion"),
        margin=dict(l=100, r=50, t=50, b=50)
    )

        st.plotly_chart(fig)

else:
    st.warning("No mood logs found yet!")