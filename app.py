import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
# Atur layout menjadi wide
st.set_page_config(layout="wide")

# Judul dashboard
st.title("Perbandingan Model Forecast dalam Prediksi Penjualan Pelumas Wilayah Surabaya")

st.write("""
Dashboard ini bertujuan untuk membandingkan berbagai model *Exponential Smoothing* 
dalam memprediksi penjualan pelumas untuk wilayah Surabaya berdasarkan nilai metrik error MAPE.
""")

st.markdown("""
### Total Forecast per Produk:
- SES (Simple Exponential Smoothing): 5 model 
  - α = [0.1, 0.3, 0.5, 0.7, 0.9]
- Holt's Linear Trend: 9 model 
  - Kombinasi α = [0.1, 0.5, 0.9] dan β = [0.1, 0.5, 0.9]
- Holt-Winters: 27 model 
  - Kombinasi α = [0.1, 0.5, 0.9], β = [0.1, 0.5, 0.9], dan γ = [0.1, 0.5, 0.9]

### Total Model per Produk:
- SES: 5 model
- Holt's Linear Trend: 9 model
- Holt-Winters: 27 model
- Total: 41 model per produk
""")

# Path folder tempat file disimpan (sesuaikan dengan direktori di VS Code)
data_folder = "D:/Dashboard_Excel"  # Ganti sesuai struktur folder di VS Code

# Tab navigasi
tab1, tab2, tab3 = st.tabs(["Backtest", "Model Terbaik", "Forecast 2025"])

# Tab 1: Backtest
with tab1:
    st.subheader("Backtest - Evaluasi Performa Model")
    st.markdown("Dataset ini berisi hasil Grid Search 41 model untuk setiap produk.")
    file_path = os.path.join(data_folder, "model_comparison_mape.xlsx")
    if os.path.exists(file_path):
        df_backtest = pd.read_excel(file_path)
        st.dataframe(df_backtest)
    else:
        st.error("File model_comparison_mape.xlsx tidak ditemukan!")

# Tab 2: Model Terbaik
with tab2:
    st.subheader("Model Terbaik per Produk")
    st.markdown("Dataset ini menunjukkan model terbaik untuk setiap produk berdasarkan nilai Average MAPE terkecil.")
    file_path = os.path.join(data_folder, "best_model_per_product.xlsx")
    if os.path.exists(file_path):
        df_best_model = pd.read_excel(file_path)
        st.dataframe(df_best_model)
    else:
        st.error("File best_model_per_product.xlsx tidak ditemukan!")

# Tambahkan pie chart Distribusi Kategori MAPE
    st.subheader("Distribusi Kategori MAPE")

# Gunakan st.columns untuk mengontrol layout
    col1, col2, col3 = st.columns([1, 2, 1])  # Pie chart ada di tengah

    with col2:  # Pie chart ada di kolom tengah agar tidak terlalu wide
        categories = ["Inaccurate", "Reasonable", "Good", "Highly Accurate"]
        values = [40.8, 29.2, 12.7, 17.3]
    
        fig, ax = plt.subplots(figsize=(6, 6))  # Ukuran lebih proporsional
        ax.pie(
            values, labels=categories, autopct='%1.1f%%', startangle=140,
            colors=["red", "orange", "yellow", "green"], textprops={'fontsize': 12}
        )
        ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
    
        st.pyplot(fig)

# Tab 3: Forecast 2025
with tab3:
    st.subheader("Forecast Penjualan Januari - Maret 2025")
    st.markdown("Dataset ini berisi prediksi penjualan untuk Januari hingga Maret 2025 berdasarkan model terbaik.")
    file_path = os.path.join(data_folder, "forecast_jan_mar_2025.xlsx")
    if os.path.exists(file_path):
        df_forecast = pd.read_excel(file_path)
        st.dataframe(df_forecast)
    else:
        st.error("File forecast_jan_mar_2025.xlsx tidak ditemukan!")
