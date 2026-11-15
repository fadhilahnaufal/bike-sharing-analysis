# Bike Sharing Data Analysis Dashboard

## Deskripsi
Proyek ini merupakan analisis data penyewaan sepeda (Bike Sharing Dataset) selama tahun 2011–2012.

Analisis dilakukan untuk mengetahui:
1. Perbedaan rata-rata jumlah penyewaan sepeda berdasarkan musim.
2. Perbedaan rata-rata jumlah penyewaan sepeda berdasarkan kondisi cuaca.
3. Pola jumlah penyewaan sepeda berdasarkan jam.
4. Hubungan kondisi cuaca dengan jumlah penyewaan sepeda per jam.

## Struktur Folder
- `dashboard/`: berisi file dashboard Streamlit.
- `data/`: berisi dataset day.csv dan hour.csv.
- `notebook.ipynb`: berisi proses analisis data.
- `requirements.txt`: berisi library yang diperlukan.

## Instalasi Library
Jalankan perintah berikut:

```bash
pip install -r requirements.txt
```

## Menjalankan Dashboard
Pastikan berada di direktori utama proyek, kemudian jalankan:

```bash
streamlit run dashboard/dashboard.py
```

## Dataset
Dataset yang digunakan adalah Bike Sharing Dataset yang terdiri dari:
- day.csv
- hour.csv

## Tools
- Python
- Pandas
- Matplotlib
- Seaborn
- Streamlit
- Jupyter Notebook / Google Colab