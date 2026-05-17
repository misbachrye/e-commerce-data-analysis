# 🛍️ E-Commerce Public Data Dashboard

Dashboard ini menyajikan analisis performa produk, demografi pelanggan, dan RFM Analysis dari E-Commerce Public Dataset.

## 🛠️ Setup Environment
Pilih salah satu metode di bawah ini untuk mengatur environment Python Anda.

**Menggunakan Anaconda (Rekomendasi)**
1. Buka terminal/command prompt.
2. Jalankan perintah berikut:
   conda create --name main-ds python=3.9
   conda activate main-ds
   pip install -r requirements.txt

**Menggunakan venv (Bawaan Python)**
1. Buka terminal/command prompt.
2. Buat virtual environment:
   python -m venv env
3. Aktifkan environment (Pilih sesuai OS Anda):
   Windows: env\Scripts\activate
   Mac/Linux: source env/bin/activate
4. Install library:
   pip install -r requirements.txt

## 🚀 Run Streamlit App
Setelah environment aktif dan semua library terinstal, jalankan perintah berikut di terminal Anda:

streamlit run dashboard.py