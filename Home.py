#importing the required modules/ functions
import os
import streamlit as st
import pandas as pd
from datetime import datetime as dt, timezone as tz, time
import pytz
from mood_utils import analyze_text
import fitz #PyMuPDF, needs anaconda's python since its installed there
import plotly.graph_objects as go
import plotly.express as px



if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(
        columns=["Timestamp","Text", 
                 "Positive", "Neutral", "Negative"]
    )

# Sidebar navigation
page = st.sidebar.radio("Navigate", ["Home", "My Logs", "My Stats"])

#theme
st.markdown("""
<style>
/* Sidebar background */
[data-testid="stSidebar"] {
    background-color: #302b28 !important;
}

/* Sidebar text */
[data-testid="stSidebar"] .css-1v3fvcr, 
[data-testid="stSidebar"] label, 
[data-testid="stSidebar"] .css-17eq0hr {
    color: "#E7DFCF" !important;
    font-weight: 600;
}

/* Radio button hover */
[data-testid="stSidebar"] .stRadio > div > label:hover {
    background-color: #F8F4E3 !important;
    border-radius: 8px;
}
@import url('https://fonts.googleapis.com/css2?family=Comfortaa:wght@400;600;700&display=swap');

    div[data-testid="stAppViewContainer"] * {
        font-family: 'Comfortaa', cursive !important;
        
    }
</style>
""", unsafe_allow_html=True)

local_tz = pytz.timezone("America/Los_Angeles")
# Show pages
if page == "Home":
    st.title("senTIME")
    st.subheader("Track your emotional tone over time")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")


    mood_map, key_words, past_wks = st.columns(3)
    with mood_map:
        st.markdown("""
    <div class='card'>
        <h4 style='color:#362706;text-align: center;'>MoodMap</h4>
        <p style='color:#2B2B2B;'>Mostly Neutral this week</p>
    </div> 
    <style>
        /* Card container */
        .card {
            background-color: #e8ac54;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #7d6a57;
            box-shadow: 2px 2px 8px rgba(0,0,0,0.03);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        /* Hover animation */
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 4px 6px 15px rgba(0, 0, 0, 0.08);
        }
        </style>               
    """, unsafe_allow_html=True)
    with key_words:
        st.markdown("""
    <div class='card'>
        <h4 style='color:#362706;text-align: center;'>MoodBot</h4>
        <p style='color:#2B2B2B;'>Mostly Neutral this week</p>
    </div> 
    <style>
        /* Card container */
        .card {
            background-color: #e8ac54;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #7d6a57;
            box-shadow: 2px 2px 8px rgba(0,0,0,0.03);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        /* Hover animation */
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 4px 6px 15px rgba(0, 0, 0, 0.08);
        }
    </style>                
    """, unsafe_allow_html=True)
    st.write("")
    st.page_link("pages/MoodMap.py", label="Learn more...",icon="🫧")
    with past_wks:
        st.markdown("""
    <div class='card'>
        <h4 style='color:#362706;text-align: center;'>MoodBloom</h4>
        <p style='color:#2B2B2B;'>Mostly Neutral this week</p>
    </div> 
    <style>
        /* Card container */
        .card {
            background-color: #e8ac54;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #7d6a57;
            box-shadow: 2px 2px 8px rgba(0,0,0,0.03);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        /* Hover animation */
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 4px 6px 15px rgba(0, 0, 0, 0.08);
        }
        </style>                
    """, unsafe_allow_html=True)

if page == "My Logs":
    st.title("📝 My Logs")
    st.subheader("New Log")

    #choosing input method
    log_method = st.radio("Choose log method...", ["Type something", "Upload a file"])
    
    if log_method=="Type something":
    #getting user input
        user_input = st.text_area("Type something...")
    else:
        log_file = st.file_uploader("Upload a text file", type=["txt", "pdf"])
        if log_file is not None and ".txt" in log_file.name:
            parse_log = log_file.read().decode("utf-8")
            user_input = st.text_area("Preview", parse_log, height=100)
        elif log_file is not None and ".pdf" in log_file.name:
            parse_pdf = fitz.open(stream=log_file.read(), filetype="pdf")
            extracted_text = ""
            for page in parse_pdf:
                extracted_text += page.get_text()
            parse_pdf.close()
            user_input = st.text_area("Preview", extracted_text, height=100)
        else:
            user_input = ""
    if st.button("Log Data"):
        if len(user_input.strip()) > 0:
            senti_scores = analyze_text(user_input)
            data_log = pd.DataFrame(
                {
                    "Timestamp": [dt.now(local_tz)],
                    "Text": [user_input],
                    "Positive": senti_scores["pos"],
                    "Neutral": senti_scores["neu"],
                    "Negative": senti_scores["neg"]
                }
            )
            logs="mood_logs.csv"
            if os.path.exists(logs):
                all_logs = pd.DataFrame(pd.read_csv(logs))
                all_logs = pd.concat([all_logs, data_log], axis=0, ignore_index=True)
                all_logs.to_csv(logs, index=False)
            else:
                data_log.to_csv("mood_logs.csv", index=False)
            #using concat for vertical stacking
            st.session_state.data = pd.concat(
                [st.session_state.data, data_log], 
                ignore_index=True
            )
            st.success("✅ Your entry has been logged successfully!")
            st.dataframe(data_log, use_container_width=True)
        else:
            st.warning("⚠️ Please check your log data and try again")
            
    st.subheader("Past Logs")
    if not st.session_state.data.empty: #if data is not empty then display the dataframe
        st.dataframe(st.session_state.data, use_container_width=True)
    else:
        st.info("No entries yet")
    
    if st.button("Clear"):
        st.session_state.data = st.session_state.data.drop(st.session_state.data.index)
        st.rerun()

elif page == "My Stats":
    st.title("📊 Your Mood Trends")
    # (Insert your plots, logs, etc.)

    tf_choice = st.selectbox("Timeframe", ["Today", "This Week", "This Month", 
                           "This Year", "Custom Dates"])
    st.write("")
    st.write("")
    positive_score = 0
    neutral_score = 0
    negative_score = 0
    fig_toggle = False
    log_path = "mood_logs.csv"

    if ("data" in st.session_state and not st.session_state.data.empty)\
        or (os.path.exists(log_path)):

        if os.path.exists(log_path):
            log_data = pd.DataFrame(pd.read_csv(log_path))
        else: ## MIGHT NOT NEED THIS, SINCE EVEN CURRENT ST.SESSION_STATE.DATA SHOULD BE IN LOG PATH
            log_data = st.session_state.data
        curr_day = dt.now(local_tz).date()
        curr_week = dt.now().isocalendar().week
        curr_month = dt.now().month
        curr_year = dt.now().year
        log_data["Timestamp"] = pd.to_datetime(log_data["Timestamp"], 
                                                   errors="coerce")
        

        stats_data = pd.read_csv("mood_logs.csv", parse_dates=["Timestamp"])
        stats_data["Date"] = stats_data["Timestamp"].dt.date


        if tf_choice == "Today":
            past_day = log_data[log_data["Timestamp"].dt.date 
                               == curr_day]
            if past_day.shape[0] != 0:
                fig_toggle = True
                avg_pos = past_day["Positive"].mean()
                avg_neu = past_day["Neutral"].mean()
                avg_neg = past_day["Negative"].mean()
                total = avg_pos + avg_neu + avg_neg
                positive_score = avg_pos/total
                neutral_score = avg_neu/total
                negative_score = avg_neg/total
                stats_data = stats_data[stats_data["Date"]==curr_day]
                stats_data = stats_data.groupby("Date")[["Positive", "Neutral", 
                                             "Negative"]].mean().reset_index()
            else:
                st.info("No log entries today!")
        elif tf_choice == "This Week":
            past_week = log_data[log_data["Timestamp"].dt.isocalendar().week 
                               == curr_week]
            if past_week.shape[0] != 0:
                fig_toggle = True
                avg_pos = past_week["Positive"].mean()
                avg_neu = past_week["Neutral"].mean()
                avg_neg = past_week["Negative"].mean()
                total = avg_pos + avg_neu + avg_neg
                positive_score = avg_pos / total
                neutral_score = avg_neu / total
                negative_score = avg_neg / total
            else:
                st.info("No log entries this week")


        elif tf_choice == "This Month":
            past_month = log_data[log_data["Timestamp"].dt.month 
                               == curr_month]
            if past_month.shape[0] != 0:
                fig_toggle = True
                avg_pos = past_month["Positive"].mean()
                avg_neu = past_month["Neutral"].mean()
                avg_neg = past_month["Negative"].mean()
                total = avg_pos + avg_neu + avg_neg
                positive_score = avg_pos/total
                neutral_score = avg_neu/total
                negative_score = avg_neg/total
            else:
                st.info("No log entries this month!")
        elif tf_choice == "This Year":
            past_year = log_data[log_data["Timestamp"].dt.year 
                               == curr_year]
            if past_year.shape[0] != 0:
                fig_toggle = True
                avg_pos = past_year["Positive"].mean()
                avg_neu = past_year["Neutral"].mean()
                avg_neg = past_year["Negative"].mean()
                total = avg_pos + avg_neu + avg_neg
                positive_score = avg_pos/total
                neutral_score = avg_neu/total
                negative_score = avg_neg/total
            else:
                st.info("No log entries this year!")
        elif tf_choice == "Custom Dates":
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
            
            custom_dates = log_data[(log_data["Timestamp"] >= start_datetime) &
                               (log_data["Timestamp"] <= end_datetime)]
            if custom_dates.shape[0] != 0:
                fig_toggle = True
                avg_pos = custom_dates["Positive"].mean()
                avg_neu = custom_dates["Neutral"].mean()
                avg_neg = custom_dates["Negative"].mean()
                total = avg_pos + avg_neu + avg_neg
                positive_score = avg_pos/total
                neutral_score = avg_neu/total
                negative_score = avg_neg/total
            else:
                st.info(f"No log entries between {start_date} and {end_date}!")
                
    else:
        st.info("Try adding a new log to see your average tone per entry!")
    if fig_toggle:
        fig = go.Figure(go.Pie(
            values=[positive_score, neutral_score, negative_score],
            labels=["Positive", "Neutral", "Negative"], #calculated using %positive sentiment??
            hole=0.6,
            marker_colors=["#e8ac54", "#d8cbb4ff", "#d27b6f"], ##F0C49A
            textinfo='label+percent',
            hoverinfo="skip",
            textfont_size=14
        ))
        fig.update_layout(
            width=500,   # width in pixels
            height=500,  # height in pixels
            margin=dict(t=20, b=20, l=20, r=20),  # optional: reduce extra white space
            #paper_bgcolor="#302b28",  # match your app background if you want
            font=dict(color="white")  # make labels visible on dark background
        )

        col1, col2, col3 = st.columns([1.5, 2, 1])
        with col2:
            st.plotly_chart(fig, use_container_width=False) 
        fig_line = px.line(stats_data,x="Date",y=["Positive",
            "Neutral","Negative"],title="Mood Trend Over Time")
        st.plotly_chart(fig_line)
    
    month_map = {
    1:"January",
    2:"February",
    3:"March",
    4:"April",
    5:"May",
    6:"June",
    7:"July",
    8:"August",
    9:"September",
    10:"October",
    11:"November",
    12:"December"
    }
    weekday_map = {
    0:"Monday", 1:"Tuesday", 2:"Wednesday",
    3:"Thursday", 4:"Friday", 5:"Saturday",
    6:"Sunday"
    }

    user_month=st.selectbox("Month", month_map.values())
    stats_data = pd.DataFrame(pd.read_csv("moodbloom.csv"))
    stats_data["date"]=stats_data["date"].apply(lambda x: 
                    pd.to_datetime(x[2:]))
    stats_data["month"] = stats_data["date"].dt.month.apply(lambda x: month_map[x])
    stats_data=stats_data[stats_data["month"]==user_month].drop(columns="month")
    dates=pd.date_range(stats_data["date"][0], stats_data["date"][len(stats_data)-1])
    falses=[False for var in range(len(stats_data.columns)-1)]
    for date in dates:
        if date not in list(stats_data["date"]):
            stats_data.loc[len(stats_data)]=[date]+falses
    stats_data=stats_data.set_index("date")
    stats_data["completion"]=stats_data.sum(axis=1)/stats_data.shape[1]
    stats_data=stats_data.reset_index()
    stats_data["week"] = stats_data["date"].dt.day.apply(lambda x: "Week 1" if x in range(1,8) else
                                                ("Week 2" if x in range(8,15) else (
                                                    "Week 3" if x in range(15,22) else 
                                                    "Week 4"))) 
    days_order=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    stats_data["weekday"]=pd.Categorical(stats_data["date"].dt.day_of_week.apply(lambda x: weekday_map[x]),
                                 categories=days_order,ordered=True)
    calendar_data=stats_data.pivot_table(columns="weekday",
                    values="completion",index="week")
    # Assuming `calendar_data` is your pivot table
    mood_warm= [
    [0.0,  "#fde9c4"],  # very light gold
    [0.16, "#f9d7a7"],  # light gold
    [0.32, "#f5c285"],  # medium gold-orange
    [0.48, "#e8a761"],  # muted orange
    [0.64, "#c97c5c"],  # soft reddish-brown
    [0.8,  "#9c4f46"],  # darker red-brown
    [1.0,  "#622c25"]   # deep brown-red
]

    
    fig_pivot = px.imshow(
        calendar_data,
        labels=dict(x="Weekday", y="Week", color="Completion"),
        color_continuous_scale=mood_warm,  # or your Moodicle palette
        aspect="auto"
    )

    fig_pivot.update_layout(
        title="September Habit Completion",
        xaxis_title="Day of Week",
        yaxis_title="Week",
        height=500, width=800
    )
    st.plotly_chart(fig_pivot)
    