import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='darkgrid')

df = pd.read_csv('all_data.csv')

df['day_dteday'] = pd.to_datetime(df['day_dteday'])
df['hour_dteday'] = pd.to_datetime(df['hour_dteday'])

season_summary = df.groupby('day_season_name')['day_cnt'].sum().sort_values(ascending=False).reset_index()

daily_season_trend = df.groupby(['day_dteday', 'day_season_name'])['day_cnt'].sum().reset_index()

hourly_trend = df.groupby(['hour_hr', 'day_season_name'])['hour_cnt'].mean().reset_index()

min_date = df['day_dteday'].min()
max_date = df['day_dteday'].max()

# Sidebar
with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png", use_column_width=True)
    st.header("Filter Data")
    start_date, end_date = st.date_input("Rentang Waktu", [min_date, max_date], min_value=min_date, max_value=max_date)

df_filtered = df[(df['day_dteday'] >= pd.to_datetime(start_date)) & (df['day_dteday'] <= pd.to_datetime(end_date))]

st.title("Dashboard Penyewaan Sepeda")

st.header("Penyewaan Sepeda Berdasarkan Musim")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=season_summary, x='day_season_name', y='day_cnt', palette='coolwarm', ax=ax)
ax.set_title('Total Penyewaan Sepeda Berdasarkan Musim')
ax.set_xlabel('Musim')
ax.set_ylabel('Jumlah Penyewaan')
st.pyplot(fig)

st.header("Tren Penyewaan Sepeda Harian Berdasarkan Musim")
daily_season_trend_filtered = df_filtered.groupby(['day_dteday', 'day_season_name'])['day_cnt'].sum().reset_index()
fig, ax = plt.subplots(figsize=(14, 7))
sns.lineplot(data=daily_season_trend_filtered, x='day_dteday', y='day_cnt', hue='day_season_name', palette='coolwarm', ax=ax)
ax.set_title('Tren Penyewaan Sepeda Harian')
ax.set_xlabel('Tanggal')
ax.set_ylabel('Jumlah Penyewaan')
ax.legend(title='Musim')
st.pyplot(fig)

st.header("Pengaruh Jam Terhadap Penyewaan Sepeda")
hourly_trend_filtered = df_filtered.groupby(['hour_hr', 'day_season_name'])['hour_cnt'].mean().reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=hourly_trend_filtered, x='hour_hr', y='hour_cnt', hue='day_season_name', palette='coolwarm', ax=ax)
ax.set_title('Rata-rata Penyewaan Sepeda Per Jam')
ax.set_xlabel('Jam')
ax.set_ylabel('Rata-rata Penyewaan')
ax.legend(title='Musim')
st.pyplot(fig)

st.caption('Dashboard ini dibuat berdasarkan analisis data penyewaan sepeda.')
