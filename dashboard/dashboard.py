import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# Title and description
st.title("Bike Sharing Dashboard")
st.markdown(
    """
    ### Analisis Data Penyewaan Sepeda
    Dashboard ini menampilkan tren penyewaan sepeda berdasarkan dataset harian dan jam.
    Dataset digunakan untuk menjawab pertanyaan bisnis terkait musim, waktu, dan tren harian.
    """
)

# Sidebar for date range selection
st.sidebar.header("Pengaturan Rentang Waktu")
default_start_date = "2011-01-01"
default_end_date = "2012-12-31"
date_range = st.sidebar.date_input(
    "Pilih rentang waktu:",
    [pd.to_datetime(default_start_date), pd.to_datetime(default_end_date)],
    min_value=pd.to_datetime(default_start_date),
    max_value=pd.to_datetime(default_end_date),
)

# File upload
uploaded_file = st.file_uploader("Upload dataset (day.csv or hour.csv)", type=["csv"])

if uploaded_file:
    # Load dataset
    data = pd.read_csv(uploaded_file)

    # Ensure necessary columns exist
    if "day_dteday" in data.columns:
        data['day_dteday'] = pd.to_datetime(data['day_dteday'])

        # Filter data by date range
        start_date, end_date = date_range
        filtered_data = data[(data['day_dteday'] >= start_date) & (data['day_dteday'] <= end_date)]

        st.write("## Data Preview")
        st.dataframe(filtered_data.head())

        # Display dataset summary
        st.write("## Data Summary")
        st.write(filtered_data.describe())

        # Visualization & Explanatory Analysis
        st.write("## Visualization & Explanatory Analysis")

        # Question 1: Season analysis
        if "season" in filtered_data.columns:
            st.write("### Musim dengan Penyewaan Terbanyak dan Tersedikit")
            season_counts = filtered_data["season"].value_counts().sort_index()
            fig, ax = plt.subplots()
            sns.barplot(x=season_counts.index, y=season_counts.values, ax=ax)
            ax.set_title("Jumlah Penyewaan Berdasarkan Musim")
            ax.set_xlabel("Musim")
            ax.set_ylabel("Jumlah Penyewaan")
            st.pyplot(fig)

        # Question 2: Daily trend by season
        if "season" in filtered_data.columns and "cnt" in filtered_data.columns:
            st.write("### Penyewaan Sepeda Harian Berdasarkan Musim")
            fig, ax = plt.subplots()
            sns.lineplot(x="day_dteday", y="cnt", hue="season", data=filtered_data, ax=ax)
            ax.set_title("Tren Penyewaan Harian Berdasarkan Musim")
            ax.set_xlabel("Tanggal")
            ax.set_ylabel("Jumlah Penyewaan")
            st.pyplot(fig)

        # Question 3: Hourly trend analysis
        if "hour" in filtered_data.columns and "cnt" in filtered_data.columns:
            st.write("### Pengaruh Jam terhadap Penyewaan Sepeda")
            hourly_data = filtered_data.groupby("hour")["cnt"].mean().reset_index()
            fig, ax = plt.subplots()
            sns.lineplot(x="hour", y="cnt", data=hourly_data, ax=ax)
            ax.set_title("Rata-rata Penyewaan Berdasarkan Jam")
            ax.set_xlabel("Jam")
            ax.set_ylabel("Rata-rata Penyewaan")
            st.pyplot(fig)

        # Additional insights
        st.write("### Insight Penting")
        st.markdown(
            "- **Musim dengan Penyewaan Terbanyak:** Musim yang paling sering muncul di grafik.\n"
            "- **Tren Harian:** Penyewaan cenderung meningkat pada musim tertentu.\n"
            "- **Jam Sibuk:** Jam-jam dengan rata-rata penyewaan tertinggi.\n"
        )
    else:
        st.error("Dataset tidak memiliki kolom 'day_dteday'. Harap upload dataset yang sesuai.")
else:
    st.info("Silakan upload file dataset untuk memulai analisis.")
