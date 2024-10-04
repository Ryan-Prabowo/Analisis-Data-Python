# Analisis-Data-Python

Proyek ini bertujuan untuk menganalisis data penggunaan sepeda dengan menggunakan teknik visualisasi data dan analisis kluster. Proyek ini menggunakan **Streamlit** sebagai framework untuk membuat dashboard interaktif, di mana pengguna dapat memilih berbagai jenis visualisasi berdasarkan data penggunaan sepeda.

## Fitur Utama:
- Heatmap rata-rata rental sepeda per jam dalam satu minggu.
- Tren penggunaan sepeda berdasarkan musim.
- Visualisasi kluster waktu berdasarkan pagi, siang, sore, malam.
- Filter interaktif untuk memilih jenis plot dan data berdasarkan tahun.




## Setup Environment - Anaconda
```
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal
```
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run steamlit app
```
streamlit run Bike_Sharing_app_Fransiscus.py.py
```
atau gunakan link berikut https://fransiscus-bikesharing.streamlit.app/
