import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Mengatur tampilan halaman Streamlit
st.set_page_config(page_title="E-Commerce Dashboard", page_icon="🛍️", layout="wide")

# ==============================
# 1. LOAD DATA & PREPROCESSING
# ==============================
@st.cache_data
def load_data():
    df = pd.read_csv("main_data.csv")
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    return df

all_df = load_data()

# ==============================
# 2. HELPER FUNCTIONS
# ==============================
def create_revenue_df(df):
    df_2018 = df[(df['order_purchase_timestamp'].dt.year == 2018) & (df['order_status'] == 'delivered')]
    revenue_df = df_2018.groupby(by='product_category_name_english').agg({
        'price': 'sum'
    }).reset_index().rename(columns={'price': 'total_revenue'})
    return revenue_df.sort_values(by='total_revenue', ascending=False)

def create_customer_state_df(df):
    state_df = df.groupby(by='customer_state').customer_id.nunique().reset_index()
    state_df = state_df.rename(columns={'customer_id': 'customer_count'})
    return state_df.sort_values(by='customer_count', ascending=False)

def create_rfm_df(df):
    recent_date = df['order_purchase_timestamp'].max() + pd.Timedelta(days=1)
    rfm_df = df.groupby('customer_unique_id').agg({
        'order_purchase_timestamp': lambda x: (recent_date - x.max()).days,
        'order_id': 'nunique',
        'price': 'sum'
    }).reset_index()
    rfm_df.columns = ['customer_unique_id', 'recency', 'frequency', 'monetary']
    return rfm_df

# ==============================
# 3. SIDEBAR (FILTERING)
# ==============================
with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    st.header("Filter Tanggal Pesanan")
    
    min_date = all_df["order_purchase_timestamp"].min().date()
    max_date = all_df["order_purchase_timestamp"].max().date()
    
    # Mengambil input tanggal dari pengguna
    date_range = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Validasi input tanggal: Pastikan pengguna sudah memilih 2 tanggal (start dan end)
if len(date_range) == 2:
    start_date, end_date = date_range
else:
    # Jika baru pilih 1 tanggal, gunakan tanggal tersebut untuk start dan end sementara
    start_date = end_date = date_range[0] 

# Filter data berdasarkan rentang waktu dari sidebar
main_df = all_df[(all_df["order_purchase_timestamp"].dt.date >= start_date) & 
                 (all_df["order_purchase_timestamp"].dt.date <= end_date)]

# ==============================
# 4. MAIN CONTENT
# ==============================
st.header("🛍️ E-Commerce Public Data Dashboard")
st.markdown("Dashboard ini menyajikan analisis performa produk, persebaran pelanggan, dan analisis RFM dari E-Commerce Public Dataset.")

# Cek apakah data kosong setelah difilter
if main_df.empty:
    st.warning("⚠️ Tidak ada data transaksi pada rentang tanggal yang Anda pilih. Silakan sesuaikan kembali filter di kalender samping.")
else:
    # Siapkan dataframe dari helper function jika data ada
    revenue_df = create_revenue_df(main_df)
    customer_state_df = create_customer_state_df(main_df)
    rfm_df = create_rfm_df(main_df)

    st.subheader("Pertanyaan Bisnis 1: Performa Revenue Produk")
    
    if revenue_df.empty:
        st.info("Tidak ada data produk berstatus 'delivered' pada rentang waktu ini untuk tahun 2018.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Top 5 Kategori Produk (Tertinggi)**")
            fig, ax = plt.subplots(figsize=(10, 6))
            colors_top = ["#1f77b4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
            
            sns.barplot(
                x="total_revenue", 
                y="product_category_name_english", 
                data=revenue_df.head(5), 
                palette=colors_top, 
                hue="product_category_name_english", 
                legend=False, 
                ax=ax
            )
            ax.set_ylabel(None)
            ax.set_xlabel("Total Revenue (BRL)")
            st.pyplot(fig)

        with col2:
            st.markdown("**Bottom 5 Kategori Produk (Terendah)**")
            fig, ax = plt.subplots(figsize=(10, 6))
            colors_bottom = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#d62728"] # INI BENAR
            
            bottom_data = revenue_df.tail(5) if len(revenue_df) >= 5 else revenue_df
            sns.barplot(
                x="total_revenue", 
                y="product_category_name_english", 
                data=bottom_data, 
                palette=colors_bottom[:len(bottom_data)], 
                hue="product_category_name_english", 
                legend=False, 
                ax=ax
            )
            ax.set_ylabel(None)
            ax.set_xlabel("Total Revenue (BRL)")
            ax.invert_xaxis()
            ax.yaxis.set_label_position("right")
            ax.yaxis.tick_right()
            st.pyplot(fig)

    st.markdown("---")
    st.subheader("Pertanyaan Bisnis 2: Demografi Pelanggan (Top 10 State)")
    fig, ax = plt.subplots(figsize=(12, 6))
    colors_state = ["#1f77b4"] + ["#D3D3D3"] * 9
    top_10_state = customer_state_df.head(10) if len(customer_state_df) >= 10 else customer_state_df
    
    sns.barplot(
        x="customer_count", 
        y="customer_state", 
        data=top_10_state, 
        palette=colors_state[:len(top_10_state)], 
        hue="customer_state", 
        legend=False, 
        ax=ax
    )
    ax.set_ylabel("State")
    ax.set_xlabel("Jumlah Pelanggan")
    st.pyplot(fig)

    st.markdown("---")
    st.subheader("Analisis Lanjutan: RFM Analysis")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Rata-rata Recency (Hari)", value=round(rfm_df.recency.mean(), 1) if not rfm_df.empty else 0)
    with col2:
        st.metric("Rata-rata Frequency (Transaksi)", value=round(rfm_df.frequency.mean(), 2) if not rfm_df.empty else 0)
    with col3:
        st.metric("Rata-rata Monetary (BRL)", value=round(rfm_df.monetary.mean(), 2) if not rfm_df.empty else 0)

    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 6))
    colors = ["#1f77b4"]

    sns.histplot(rfm_df['recency'], bins=50, color=colors[0], ax=ax[0], kde=True)
    ax[0].set_title("Distribusi Recency", fontsize=15)

    sns.countplot(x='frequency', data=rfm_df[rfm_df['frequency'] <= 5], color=colors[0], ax=ax[1])
    ax[1].set_title("Distribusi Frequency", fontsize=15)

    sns.histplot(rfm_df['monetary'], bins=50, color=colors[0], ax=ax[2], kde=True)
    ax[2].set_title("Distribusi Monetary", fontsize=15)
    
    # Hanya set xlim jika ada data
    if not rfm_df.empty and rfm_df['monetary'].quantile(0.95) > 0:
        ax[2].set_xlim(0, rfm_df['monetary'].quantile(0.95)) 

    st.pyplot(fig)

st.caption("Hak Cipta © Ahmad Misbach 2026")
