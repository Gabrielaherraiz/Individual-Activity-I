import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import time
import random

sheet_url = "https://docs.google.com/spreadsheets/d/1lCeoifXWJ749Uaf5vVYBn__F6qubHdqa5XJYFNkbgXg/gviz/tq?tqx=out:csv"

try:
    df = pd.read_csv(sheet_url)
    df.dropna(inplace=True)  
except Exception as e:
    st.error(f"Error connecting to Google Sheets: {str(e)}")
    df = None

if df is not None:
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df.dropna(inplace=True)

    st.title("Individual Activity I: A/B Testing with Diamonds Dataset")
    
    st.markdown("""
    ### 📝 About This Activity
    In this experiment, we will conduct an **A/B test** using data from a diamonds dataset.  
    You will be shown **one visualization at random**, and your task is to determine **whether it effectively answers the business question**.

    The experiment will measure:
    - Your **reaction time** (how long it takes to analyze the data).
    - How different visualization techniques help in decision-making.

    ### 💎 Understanding the Dataset
    Diamonds are evaluated based on several factors, including:
    - **Cut Quality**: How well the diamond has been cut and polished.
    - **Price**: The cost in dollars.
    
    **Our analysis will focus on understanding how cut quality affects pricing and overall diamond value.**  
    """)

    st.subheader("🔍 Business Question: How does cut quality affect diamond pricing?")

    if 'chart_shown' not in st.session_state:
        st.session_state.chart_shown = False
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'selected_chart' not in st.session_state:
        st.session_state.selected_chart = None

    graph_options = ["bar", "box"]
    
    if st.button("Show a Random Chart"):
        st.session_state.selected_chart = random.choice(graph_options)
        st.session_state.chart_shown = True
        st.session_state.start_time = time.time()

    if st.session_state.chart_shown:
        st.markdown(f"**{st.session_state.selected_chart.capitalize()} Chart**")
        fig, ax = plt.subplots(figsize=(7, 5))
        
        if st.session_state.selected_chart == "bar":
            cut_counts = df["cut"].value_counts()
            sns.barplot(x=cut_counts.index, y=cut_counts.values, palette="Blues_r", ax=ax)
            ax.set_xlabel("Cut")
            ax.set_ylabel("Count")
            ax.set_title("Distribution of Diamond Cuts")

        elif st.session_state.selected_chart == "box":
            sns.boxplot(x="cut", y="price", data=df, palette="coolwarm", ax=ax)
            ax.set_xlabel("Cut")
            ax.set_ylabel("Price")
            ax.set_title("Price Distribution by Diamond Cut")
            ax.set_yscale("log")
        
        st.pyplot(fig)

        if st.button("I answered your question"):
            time_taken = time.time() - st.session_state.start_time
            st.success(f"✅ You took {time_taken:.2f} seconds to answer.")
