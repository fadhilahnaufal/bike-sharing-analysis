import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

sns.set_theme(style="whitegrid")

st.title("🚲 Bike Sharing Data Dashboard")
st.write(
    "Dashboard analisis penyewaan sepeda berdasarkan musim, "
    "kondisi cuaca, dan jam penyewaan selama tahun 2011–2012."
)

# Memuat dataset
@st.cache_data
def load_data():
    day_df = pd.read_csv("day.csv")
    hour_df = pd.read_csv("hour.csv")

    day_df["dteday"] = pd.to_datetime(day_df["dteday"])
    hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

    season_map = {
        1: "Spring",
        2: "Summer",
        3: "Fall",
        4: "Winter"
    }

    weather_map = {
        1: "Cerah",
        2: "Berawan/Kabut",
        3: "Hujan ringan",
        4: "Cuaca buruk"
    }

    for df in [day_df, hour_df]:
        df["season_label"] = df["season"].map(season_map)
        df["weather_label"] = df["weathersit"].map(weather_map)

    return day_df, hour_df


day_df, hour_df = load_data()

# Filter tanggal interaktif
st.sidebar.header("🔍 Filter Rentang Waktu")

min_date = day_df["dteday"].min().date()
max_date = day_df["dteday"].max().date()

date_range = st.sidebar.date_input(
    "Pilih rentang tanggal",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(date_range) != 2:
    st.info("Silakan pilih tanggal awal dan tanggal akhir.")
    st.stop()

start_date, end_date = date_range

if start_date > end_date:
    st.error("Tanggal awal tidak boleh melewati tanggal akhir.")
    st.stop()

main_day_df = day_df[
    (day_df["dteday"].dt.date >= start_date) &
    (day_df["dteday"].dt.date <= end_date)
].copy()

main_hour_df = hour_df[
    (hour_df["dteday"].dt.date >= start_date) &
    (hour_df["dteday"].dt.date <= end_date)
].copy()

if main_day_df.empty or main_hour_df.empty:
    st.warning("Tidak ada data pada rentang tanggal tersebut.")
    st.stop()

st.caption(
    f"Periode analisis: {start_date} sampai {end_date}"
)

# Ringkasan data
st.subheader("📊 Ringkasan Penyewaan")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Penyewaan Harian",
    f"{main_day_df['cnt'].sum():,}"
)

col2.metric(
    "Rata-rata Penyewaan Harian",
    f"{main_day_df['cnt'].mean():,.0f}"
)

col3.metric(
    "Total Penyewaan Per Jam",
    f"{main_hour_df['cnt'].sum():,}"
)

st.divider()

# EDA
st.header("1. Exploratory Data Analysis")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.histplot(main_day_df["cnt"], bins=25, kde=True, ax=ax)
    ax.set_title("Distribusi Penyewaan Sepeda Harian")
    ax.set_xlabel("Jumlah Penyewaan")
    st.pyplot(fig)
    plt.close(fig)

with col2:
    corr = main_day_df[
        ["temp", "atemp", "hum", "windspeed", "casual", "registered", "cnt"]
    ].corr()

    fig, ax = plt.subplots(figsize=(7, 4))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    ax.set_title("Korelasi Variabel")
    st.pyplot(fig)
    plt.close(fig)

st.divider()

# Pertanyaan bisnis 1
st.header("2. Analisis Musim dan Kondisi Cuaca")

st.subheader("Pertanyaan Bisnis 1")
st.write(
    "Bagaimana perbedaan rata-rata penyewaan sepeda berdasarkan "
    "kombinasi musim dan kondisi cuaca?"
)

season_weather = (
    main_day_df.groupby(["season_label", "weather_label"])["cnt"]
    .mean()
    .reset_index()
)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    data=season_weather,
    x="season_label",
    y="cnt",
    hue="weather_label",
    ax=ax
)
ax.set_title("Rata-rata Penyewaan Berdasarkan Musim dan Cuaca")
ax.set_xlabel("Musim")
ax.set_ylabel("Rata-rata Penyewaan")
ax.legend(title="Kondisi Cuaca")
st.pyplot(fig)
plt.close(fig)

highest = season_weather.loc[season_weather["cnt"].idxmax()]
lowest = season_weather.loc[season_weather["cnt"].idxmin()]

col1, col2 = st.columns(2)

col1.metric(
    "Kombinasi Tertinggi",
    f"{highest['cnt']:,.0f}",
    f"{highest['season_label']} - {highest['weather_label']}"
)

col2.metric(
    "Kombinasi Terendah",
    f"{lowest['cnt']:,.0f}",
    f"{lowest['season_label']} - {lowest['weather_label']}"
)

with st.expander("Lihat penjelasan analisis musim dan cuaca"):
    st.write(
        "Rata-rata penyewaan tertinggi menunjukkan kombinasi musim "
        "dan cuaca dengan permintaan paling besar. "
        "Kondisi ini dapat menjadi pertimbangan untuk alokasi armada."
    )
    st.write(
        "Kombinasi dengan rata-rata terendah dapat menjadi sasaran "
        "promosi untuk meningkatkan penyewaan."
    )

st.divider()

# Pertanyaan bisnis 2
st.header("3. Analisis Pola Penyewaan Berdasarkan Jam")

st.subheader("Pertanyaan Bisnis 2")
st.write(
    "Pada jam berapa rata-rata penyewaan sepeda mencapai "
    "tiga nilai tertinggi dan tiga nilai terendah?"
)

hour_analysis = (
    main_hour_df.groupby("hr")["cnt"]
    .mean()
    .reset_index(name="rata_rata_penyewaan")
)

top_three = hour_analysis.nlargest(3, "rata_rata_penyewaan")
bottom_three = hour_analysis.nsmallest(3, "rata_rata_penyewaan")

fig, ax = plt.subplots(figsize=(11, 5))
sns.lineplot(
    data=hour_analysis,
    x="hr",
    y="rata_rata_penyewaan",
    marker="o",
    ax=ax
)
ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Jam")
ax.set_xlabel("Jam")
ax.set_ylabel("Rata-rata Penyewaan")
ax.set_xticks(range(24))
st.pyplot(fig)
plt.close(fig)

col1, col2 = st.columns(2)

with col1:
    st.write("**Tiga Jam dengan Penyewaan Tertinggi**")
    st.dataframe(
        top_three.sort_values(
            "rata_rata_penyewaan", ascending=False
        ).reset_index(drop=True),
        use_container_width=True
    )

with col2:
    st.write("**Tiga Jam dengan Penyewaan Terendah**")
    st.dataframe(
        bottom_three.sort_values(
            "rata_rata_penyewaan"
        ).reset_index(drop=True),
        use_container_width=True
    )

with st.expander("Lihat penjelasan pola penyewaan per jam"):
    st.write(
        "Jam dengan permintaan tertinggi dapat menjadi prioritas "
        "distribusi sepeda agar ketersediaan armada tetap terjaga."
    )
    st.write(
        "Jam dengan permintaan terendah dapat dimanfaatkan untuk "
        "perawatan dan pemeriksaan armada."
    )

st.divider()

# Kesimpulan dan rekomendasi
st.header("4. Kesimpulan dan Rekomendasi")

st.markdown("""
**Kesimpulan:**
- Musim dan kondisi cuaca berhubungan dengan perubahan jumlah penyewaan.
- Permintaan penyewaan berbeda pada setiap jam.
- Filter tanggal memungkinkan pengguna membandingkan periode analisis.

**Rekomendasi:**
- Menambah ketersediaan sepeda pada jam permintaan tinggi.
- Menjadwalkan perawatan pada jam permintaan rendah.
- Menggunakan promosi untuk meningkatkan permintaan pada periode sepi.
- Menyesuaikan alokasi armada dengan kondisi cuaca dan musim.
""")

st.caption("Bike Sharing Dataset | Analisis periode 2011–2012")
