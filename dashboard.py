
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi halaman
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    layout="wide"
)

# Membaca dataset
day_df = pd.read_csv('data/day.csv')
hour_df = pd.read_csv('data/hour.csv')

# Judul dashboard
st.title("Bike Sharing Dashboard")
st.markdown("Dashboard analisis penyewaan sepeda tahun 2011–2012")

# Ringkasan Statistik
st.subheader("Ringkasan Statistik")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Data Harian", f"{len(day_df):,}")

with col2:
    st.metric("Total Data Per Jam", f"{len(hour_df):,}")

with col3:
    st.metric(
        "Rata-rata Penyewaan Harian",
        f"{day_df['cnt'].mean():,.0f}"
    )

# Rata-rata penyewaan berdasarkan musim
st.subheader("Rata-rata Penyewaan Sepeda Berdasarkan Musim")

season_avg = day_df.groupby('season')['cnt'].mean()

season_avg.index = ['Spring', 'Summer', 'Fall', 'Winter']

fig, ax = plt.subplots()
season_avg.plot(kind='bar', ax=ax, color='skyblue')

ax.set_xlabel("Musim")
ax.set_ylabel("Rata-rata Penyewaan")
ax.set_title("Penyewaan Sepeda Berdasarkan Musim")
ax.tick_params(axis='x', rotation=0)

st.pyplot(fig)

# Rata-rata penyewaan berdasarkan kondisi cuaca
st.subheader("Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca")

weather_avg = day_df.groupby('weathersit')['cnt'].mean()

weather_avg.index = [
    'Cerah',
    'Berawan',
    'Hujan Ringan'
]

fig, ax = plt.subplots()
weather_avg.plot(kind='bar', ax=ax, color='lightgreen')

ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Rata-rata Penyewaan")
ax.set_title("Penyewaan Sepeda Berdasarkan Kondisi Cuaca")
ax.tick_params(axis='x', rotation=0)

st.pyplot(fig)

# Rata-rata penyewaan berdasarkan jam
st.subheader("Rata-rata Penyewaan Sepeda Berdasarkan Jam")

hour_avg = hour_df.groupby('hr')['cnt'].mean()

fig, ax = plt.subplots()
hour_avg.plot(kind='line', marker='o', ax=ax, color='orange')

ax.set_xlabel("Jam")
ax.set_ylabel("Rata-rata Penyewaan")
ax.set_title("Penyewaan Sepeda Berdasarkan Jam")
ax.set_xticks(range(24))
ax.grid(True)

st.pyplot(fig)

# Rata-rata penyewaan berdasarkan kondisi cuaca per jam
st.subheader("Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca (Per Jam)")

weather_hour_avg = hour_df.groupby('weathersit')['cnt'].mean()

weather_hour_avg.index = [
    'Cerah',
    'Berawan',
    'Hujan Ringan',
    'Hujan Lebat'
]

fig, ax = plt.subplots()
weather_hour_avg.plot(kind='bar', ax=ax, color='lightcoral')

ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Rata-rata Penyewaan")
ax.set_title("Penyewaan Sepeda Berdasarkan Kondisi Cuaca")
ax.tick_params(axis='x', rotation=0)

st.pyplot(fig)
