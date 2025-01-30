import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt

# Atur layout menjadi "wide"
st.set_page_config(layout="wide", page_title="Dashboard Forecast Pelumas Surabaya")

# Sidebar untuk navigasi dan unggah file
with st.sidebar:
    st.header("  ")
    st.markdown("### Unggah File")
    uploaded_file = st.file_uploader("Upload hasil grid search (CSV):", type="csv")
    uploaded_comparison_file = st.file_uploader("Upload hasil perbandingan model terbaik (Excel):", type="xlsx")
    detailed_file = st.file_uploader("Upload dataset model_comparison_detailed (Excel):", type="xlsx")
    uploaded_forecast_file = st.file_uploader("Upload dataset forecast Januari-Maret 2025 (Excel):", type="xlsx")

# Judul utama
st.title("Perbandingan Model Forecast dalam Prediksi Penjualan Pelumas Wilayah Surabaya")
st.write("""
Dashboard ini bertujuan untuk membandingkan berbagai model **Exponential Smoothing** 
dalam memprediksi penjualan pelumas untuk wilayah Surabaya berdasarkan nilai metrik error MAE dan RMSE.
""")

st.markdown("""
### Total Forecast per Produk:
- *SES (Simple Exponential Smoothing)*: 5 model 
  - α = [0.1, 0.3, 0.5, 0.7, 0.9]
- *Holt's Linear Trend*: 9 model 
  - Kombinasi α = [0.1, 0.5, 0.9] dan β = [0.1, 0.5, 0.9]
- *Holt-Winters*: 9 model 
  - Kombinasi α = [0.1, 0.5, 0.9], β = [0.1, 0.5, 0.9], dan γ = [0.1, 0.5, 0.9]

### Total Model per Produk:
- *SES*: 5 model
- *Holt's Linear Trend*: 9 model
- *Holt-Winters*: 9 model
- *Total*: 23 model per produk
""")

st.markdown("""
### Menu """)

# Fungsi untuk menentukan model terbaik berdasarkan metrik error
def get_best_model(data, metric):
    return data.loc[data.groupby('ID')[metric].idxmin()]

# Fungsi untuk menghitung persentase model terbaik
def calculate_model_percentage(data):
    all_models = ["SES", "Holt", "Holt-Winters"]
    model_counts = data["Model"].str.split("_").str[0].value_counts()
    model_counts = model_counts.reindex(all_models, fill_value=0)
    total = model_counts.sum()
    percentages = (model_counts / total * 100).round(2)
    return percentages

# Fungsi untuk menampilkan visualisasi data
def display_visualization(df, key_prefix):
    selected_id = st.selectbox(
        "Pilih ID untuk melihat detail prediksi:",
        df["ID"].unique(),
        key=f"{key_prefix}_selectbox"
    )
    id_data = df[df["ID"] == selected_id]
    if not id_data.empty:
        fig, ax = plt.subplots()
        actual = id_data[['Actual Oct', 'Actual Nov', 'Actual Dec']].values.flatten()
        forecast = id_data[['Forecast Oct', 'Forecast Nov', 'Forecast Dec']].values.flatten()
        ax.plot(actual, label="Actual", marker="o")
        ax.plot(forecast, label="Forecast", marker="x")
        ax.set_title(f"Forecast vs Actual untuk ID: {selected_id}")
        ax.legend()
        st.pyplot(fig)
    else:
        st.warning("Data untuk ID tersebut tidak ditemukan.")

# Tabs untuk mengatur tampilan halaman
tab1, tab2, tab3, tab4 = st.tabs(["Grid Search", "Perbandingan Model", "Forecast 2025", "Visualisasi Data"])

# Tab 1: Grid Search
with tab1:
    st.subheader("Hasil Grid Search")
    if uploaded_file:
        results_df = pd.read_csv(uploaded_file)
        st.dataframe(results_df)

        metric_option = st.selectbox("Pilih metrik untuk menentukan model terbaik:", ["MAE", "RMSE"], key="grid_search_metric")
        best_models = get_best_model(results_df, metric_option)

        st.write(f"Model terbaik untuk setiap ID berdasarkan {metric_option}:")
        st.dataframe(best_models)

        st.markdown("### Persentase Hasil Pemilihan Metode Forecast")
        model_percentages = calculate_model_percentage(best_models)
        fig = px.pie(
            values=model_percentages.values,
            names=model_percentages.index,
            title=f"Persentase Model Terbaik berdasarkan {metric_option}"
        )
        st.plotly_chart(fig)
    else:
        st.warning("Silakan unggah file hasil grid search untuk melanjutkan.")

# Tab 2: Perbandingan Model
with tab2:
    st.subheader("Perbandingan Model Terbaik")
    if uploaded_comparison_file:
        comparison_df = pd.read_excel(uploaded_comparison_file)
        st.dataframe(comparison_df)

        search_id_comparison = st.text_input(
            "Cari berdasarkan ID (Perbandingan Model Terbaik):",
            key="comparison_text_input"
        )
        if search_id_comparison:
            filtered_data = comparison_df[comparison_df["ID"].astype(str) == search_id_comparison]
            if not filtered_data.empty:
                st.write(f"Detail untuk ID: {search_id_comparison}")
                st.dataframe(filtered_data[[
                    'ID', 'Best Model', 'Forecast Oct', 'Forecast Nov', 'Forecast Dec',
                    'Actual Oct', 'Actual Nov', 'Actual Dec',
                    'Diff Oct', 'Diff Nov', 'Diff Dec'
                ]])
            else:
                st.warning("ID tidak ditemukan.")
    else:
        st.warning("Silakan unggah file hasil perbandingan model untuk melanjutkan.")
    
    # Jika file Excel model_comparison_detailed diupload
    if detailed_file is not None:
        # Membaca file Excel
        detailed_df = pd.read_excel(detailed_file)
        
        # Menampilkan tabel dataset
        st.write("Tabel Model Comparison Detailed:")
        st.dataframe(detailed_df)
    else:
        st.warning("Silakan unggah file dataset model_comparison_detailed untuk melihat detail.")


# Tab 3: Forecast 2025
with tab3:
    st.subheader("Forecast 2025")
    if uploaded_forecast_file:
        forecast_data = pd.read_excel(uploaded_forecast_file)
        st.dataframe(forecast_data)

        search_id_forecast = st.text_input(
            "Cari berdasarkan ID (Forecast Januari-Maret 2025):",
            key="forecast_text_input"
        )
        if search_id_forecast:
            search_results = forecast_data[forecast_data["ID"].astype(str) == search_id_forecast]
            if not search_results.empty:
                st.write(f"Hasil pencarian untuk ID: {search_id_forecast}")
                st.dataframe(search_results)
            else:
                st.warning("ID tidak ditemukan.")
    else:
        st.warning("Silakan unggah file dataset forecast untuk melanjutkan.")

# Tab 4: Visualisasi Data
with tab4:
    st.subheader("Visualisasi Data")
    if uploaded_comparison_file:
        comparison_df = pd.read_excel(uploaded_comparison_file)
        display_visualization(comparison_df, "visualization")
    else:
        st.warning("Silakan unggah file perbandingan model untuk melihat visualisasi.")
