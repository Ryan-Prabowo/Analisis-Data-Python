import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Load dataset
df_day = pd.read_csv('day.csv')  # Pastikan file ada di direktori yang benar
df_hour = pd.read_csv('hour.csv')

# Konversi kolom 'dteday' menjadi tipe datetime
df_day['dteday'] = pd.to_datetime(df_day['dteday'])
df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])

# Judul aplikasi
st.title("Analisis Bike Sharing by Fransiscus Xaverius Ryan Prabowo")

# Sidebar untuk filter tanggal (tahun) dan jenis plot
st.sidebar.header('Filter')

# Filter Tahun (Checkbox untuk memilih beberapa tahun sekaligus)
year_options = df_day['dteday'].dt.year.unique().tolist()
selected_years = st.sidebar.multiselect('Pilih Tahun', year_options, default=year_options)

# Filter Bulan (Slider untuk memilih rentang bulan)
selected_month_range = st.sidebar.slider('Pilih Rentang Bulan', 1, 12, (1, 12))

# Filter Plot
plot_options = [
    'Heatmap Rata-Rata Rental Sepeda per Jam dalam Satu Minggu',
    'Tren Perental Berdasarkan Musim',
    'Clustering Pagi Siang Sore Malam',
    'Rata-Rata Perental Sepeda Berdasarkan Kluster Waktu dan Jenis Hari'
]
selected_plot = st.sidebar.selectbox('Pilih Plot', plot_options)

# Filter data berdasarkan tahun yang dipilih dan rentang bulan
df_day_filtered = df_day[(df_day['dteday'].dt.year.isin(selected_years)) & 
                         (df_day['dteday'].dt.month.between(selected_month_range[0], selected_month_range[1]))]
df_hour_filtered = df_hour[(df_hour['dteday'].dt.year.isin(selected_years)) & 
                           (df_hour['dteday'].dt.month.between(selected_month_range[0], selected_month_range[1]))]

# Helper function untuk plot
def plot_visualization(selected_plot):
    if selected_plot == 'Heatmap Rata-Rata Rental Sepeda per Jam dalam Satu Minggu':
        # Heatmap rata-rata perental sepeda dalam waktu per jam dalam satu minggu
        plt.figure(figsize=(12, 6))
        heatmap_data = df_hour_filtered.pivot_table(values='cnt', index='weekday', columns='hr', aggfunc='mean')
        sns.heatmap(heatmap_data, cmap='Blues', annot=False)
        plt.title('Rata-Rata Rental Sepeda per Jam dalam Satu Minggu')
        plt.xlabel('Jam')
        plt.ylabel('Hari dalam Seminggu')
        plt.xticks(rotation=0)
        plt.yticks([0, 1, 2, 3, 4, 5, 6], ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'])
        st.pyplot(plt)

    elif selected_plot == 'Tren Perental Berdasarkan Musim':
        # Menghitung tren perental berdasarkan musim
        season_summary = df_day_filtered.groupby('season')[['casual', 'registered', 'cnt']].sum().reset_index()

        # Set ukuran gambar untuk semua plot
        plt.figure(figsize=(15, 15))

        # Definisikan label musim dan palet warna yang sama untuk digunakan di setiap plot
        season_labels = ['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin']
        palette1 = sns.color_palette("Set1", 4)
        palette2 = sns.color_palette("Set2", 4)
        palette3 = sns.color_palette("Set3", 4)

        # Buat legenda secara manual
        legend_patches = [mpatches.Patch(color=palette1[i], label=season_labels[i]) for i in range(4)]

        # Bar Chart untuk Casual
        plt.subplot(3, 1, 1)  # 3 baris, 1 kolom, subplot ke-1
        sns.barplot(x='season', y='casual', data=season_summary, palette=palette1)
        plt.title('Total Perental Tetap Berdasarkan Musim')
        plt.xlabel('Musim')
        plt.ylabel('Pelanggan Tetap')
        plt.legend(handles=legend_patches, title='Musim', loc='upper left')

        # Bar Chart untuk Registered
        plt.subplot(3, 1, 2)  # 3 baris, 1 kolom, subplot ke-2
        sns.barplot(x='season', y='registered', data=season_summary, palette=palette2)
        plt.title('Total Perental Baru Berdasarkan Musim')
        plt.xlabel('Musim')
        plt.ylabel('Perental Baru')
        legend_patches = [mpatches.Patch(color=palette2[i], label=season_labels[i]) for i in range(4)]
        plt.legend(handles=legend_patches, title='Musim', loc='upper left')

        # Bar Chart untuk Count
        plt.subplot(3, 1, 3)  # 3 baris, 1 kolom, subplot ke-3
        sns.barplot(x='season', y='cnt', data=season_summary, palette=palette3)
        plt.title('Total Perental Sepeda Berdasarkan Musim')
        plt.xlabel('Musim')
        plt.ylabel('Perental Sepeda')
        legend_patches = [mpatches.Patch(color=palette3[i], label=season_labels[i]) for i in range(4)]
        plt.legend(handles=legend_patches, title='Musim', loc='upper left')

        # Atur layout agar tidak overlap
        plt.tight_layout()
        st.pyplot(plt)


    elif selected_plot == 'Clustering Pagi Siang Sore Malam':
        # Clustering pagi siang sore malam
        def assign_time_cluster(hour):
            if 0 < hour <= 10:
                return 'Pagi'
            elif 10 < hour <= 15:
                return 'Siang'
            elif 15 < hour <= 18:
                return 'Sore'
            else:
                return 'Malam'

        df_hour_filtered['time_cluster'] = df_hour_filtered['hr'].apply(assign_time_cluster)
        weekday_mapping = {0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'}
        df_hour_filtered['day_cluster'] = df_hour_filtered['weekday'].map(weekday_mapping)
        day_order = ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']
        df_hour_filtered['day_cluster'] = pd.Categorical(df_hour_filtered['day_cluster'], categories=day_order, ordered=True)

        cluster_analysis = df_hour_filtered.groupby(['time_cluster', 'day_cluster'])['cnt'].mean().reset_index()

        plt.figure(figsize=(12, 6))
        sns.barplot(x='time_cluster', y='cnt', hue='day_cluster', data=cluster_analysis, palette='Set2')
        plt.title('Rata-rata Perental Sepeda Berdasarkan Cluster Waktu Dalam Satu Minggu')
        plt.xlabel('Cluster Waktu')
        plt.ylabel('Perental Sepeda')
        plt.legend(title='Hari', loc='upper left')
        st.pyplot(plt)

    elif selected_plot == 'Rata-Rata Perental Sepeda Berdasarkan Kluster Waktu dan Jenis Hari':
        # Terapkan fungsi untuk clustering waktu
        def assign_time_cluster(hour):
            if 0 < hour <= 10:
                return 'Pagi'
            elif 10 < hour <= 15:
                return 'Siang'
            elif 15 < hour <= 18:
                return 'Sore'
            else:
                return 'Malam'

        df_hour_filtered['time_cluster'] = df_hour_filtered['hr'].apply(assign_time_cluster)

        # Membuat kolom 'day_cluster' berdasarkan hari dalam seminggu
        df_hour_filtered['day_cluster'] = df_hour_filtered['weekday'].apply(lambda x: 'Hari Kerja' if x < 5 else 'Akhir Pekan')

        # Analisis dan Visualisasi Penggunaan Sepeda Berdasarkan Cluster
        cluster_analysis = df_hour_filtered.groupby(['time_cluster', 'day_cluster'])['cnt'].mean().reset_index()

        # Visualisasi: Bar Plot untuk Penggunaan Sepeda Berdasarkan Kluster Waktu dan Hari
        plt.figure(figsize=(10, 6))
        sns.barplot(x='time_cluster', y='cnt', hue='day_cluster', data=cluster_analysis, palette='Set2')
        plt.title('Rata-rata Perental Sepeda Berdasarkan Kluster Waktu dan Jenis Hari')
        plt.xlabel('Kluster Waktu')
        plt.ylabel('Rata-rata Perental Sepeda')
        plt.legend(title='Jenis Hari', loc='upper left')
        st.pyplot(plt)

# Menampilkan plot berdasarkan filter
plot_visualization(selected_plot)

st.caption('Fransiscus Xaverius Ryan Prabowo')
