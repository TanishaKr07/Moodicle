import streamlit as st
import pandas as pd
from streamlit_lottie import st_lottie
import json
import os
from datetime import datetime as dt

#st.set_page_config(page_title="Mood Bloom", layout="centered")
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

seeds = load_lottiefile("assets/animations/seeds.json")
seedling = load_lottiefile("assets/animations/seedling.json")
plant = load_lottiefile("assets/animations/plant.json")
flower = load_lottiefile("assets/animations/flower.json")

path = "moodbloom.csv"
checks = ["workout", "sleep", "water", "food", "walk", "meditation",
          "screentime", "gratitude", "connect", "nature", "song",
          "creative"]
today_date = dt.today().date().strftime("d_%Y-%m-%d")
if os.path.exists(path):
    moodbloom_df = pd.DataFrame(pd.read_csv(path,index_col="date"))
    if today_date not in list(moodbloom_df.index):
        today_habits={checks[i]: 0 for i in range(len(checks))}
    else:
        today_habits = moodbloom_df.loc[today_date]
    habit_vals = {checks[i]:today_habits[checks[i]] for i in range(len(checks))}
else:
    moodbloom_df = pd.DataFrame(columns=["date"] + checks).set_index("date")
    habit_vals = {checks[i]: 0 for i in range(len(checks))}
with st.container():
    st.subheader("Daily Checklist 🌱")
    st.write("Track your daily mood-lifting habits and watch your plant grow!")
    st.write("")

    col1,col2 = st.columns([1,1.5])

    with col1:
        habits = {
            "workout": st.checkbox("🏋️ Did a short workout", key="workout", 
                                   value=habit_vals["workout"]),
            "sleep": st.checkbox("🛌 Got 7+ hours of sleep last night", key="sleep",
                                 value=habit_vals["sleep"]),
            "water": st.checkbox("💧 Drank 8+ glasses of water", key="water",
                                 value=habit_vals["water"]),
            "food": st.checkbox("🍛 Ate a balanced meal", key="food",
                                value=habit_vals["food"]),
            "walk": st.checkbox("🚶 Went for a 15+ minute walk or stretching", key="walk",
                                value=habit_vals["walk"]),
            "meditation": st.checkbox("🧘 Practiced 5+ minutes of mindfulness or meditation", 
                                      key="meditation",value=habit_vals["meditation"]),
            "screentime": st.checkbox("📱 Limited social media use", key="screentime",
                                      value=habit_vals["screentime"]),
            "gratitude": st.checkbox("🙏 Expressed gratitude", key="gratitude", 
                                     value=habit_vals["gratitude"]),
            "connect": st.checkbox("🤗 Connected with a friend", key="connect",
                                   value=habit_vals["connect"]),
            "nature": st.checkbox("🌻 Spent time in nature, sunlight, or with pets", key="nature",
                                  value=habit_vals["nature"]),
            "song": st.checkbox("🎶 Listened to a favorite song or podcast", key="song",
                                value=habit_vals["song"]),
            "creative": st.checkbox("🎨 Engaged in a hobby or tried something new", key="creative",
                                    value=habit_vals["creative"])
        }
        for habit in habit_vals:
            habit_vals[habit]=habits[habit]
        moodbloom_df.loc[today_date]=habit_vals
        moodbloom_df.to_csv(path, index=True)

    with col2:
        habits_checked = sum(habits.values())
        if habits_checked <= 3:
            st_lottie(seeds, height=300, key="seeds")
        elif habits_checked <= 6:
            st_lottie(seedling, height=300, key="seedling")
        elif habits_checked <= 9:
            st_lottie(plant, height=300, key="plant")
        else:
            st_lottie(flower, height=300, key="flower")

        
        st.markdown(
        f"<div style='text-align: center; padding-top: 10px;'>"
        f"Progress: {habits_checked}/{len(habits)} habits completed 🌟"
        f"</div>",
        unsafe_allow_html=True
    )