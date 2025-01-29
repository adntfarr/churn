import streamlit as st
import pandas as pd
import pickle
from PIL import Image

# Load Model
model_path = "rf_ros_pca_model.pkl"
data_path = "data_oversampled.csv"

# Load the model
with open(model_path, 'rb') as file:
    model = pickle.load(file)

# Set page config
st.set_page_config(page_title="Predict Churn", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
        /* Background */
        .stApp {
            background-color: #00172B;
            color: white;
        }
        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #0E1117;
        }
        [data-testid="stSidebar"] .css-hxt7ib {
            color: white;
        }
        /* Center alignment for dashboard */
        .center-content {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("⚡Predict Churn")
menu = st.sidebar.selectbox("", ["Prediksi", "Akurasi", "Dataset", "Tentang Sistem"], index=0)

if menu == "Prediksi":
    st.title("Prediksi Customer Churn")
    st.write("Masukkan data pelanggan untuk melakukan prediksi.")
    
    # Input fitur dibagi ke dalam 3 kolom 
    col1, col2, col3 = st.columns(3)

    with col1:
        gender = st.selectbox("Gender", ["Pilih...", "Male", "Female"])
        SeniorCitizen = st.selectbox("Senior Citizen", ["Pilih...", "Yes", "No"])
        Partner = st.selectbox("Partner", ["Pilih...", "Yes", "No"])
        Dependents = st.selectbox("Dependents", ["Pilih...", "Yes", "No"])
        tenure = st.number_input("Tenure", min_value=0, max_value=10000, step=1, value=0)
        PhoneService = st.selectbox("Phone Service", ["Pilih...", "Yes", "No"])

    with col2:
        MultipleLines = st.selectbox("Multiple Lines", ["Pilih...", "Yes", "No", "No phone service"])
        InternetService = st.selectbox("Internet Service", ["Pilih...", "DSL", "Fiber optic", "No"])
        OnlineSecurity = st.selectbox("Online Security", ["Pilih...", "Yes", "No", "No internet service"])
        OnlineBackup = st.selectbox("Online Backup", ["Pilih...", "Yes", "No", "No internet service"])
        DeviceProtection = st.selectbox("Device Protection", ["Pilih...", "Yes", "No", "No internet service"])
        TechSupport = st.selectbox("Tech Support", ["Pilih...", "Yes", "No", "No internet service"])

    with col3:
        StreamingTV = st.selectbox("Streaming TV", ["Pilih...", "Yes", "No", "No internet service"])
        StreamingMovies = st.selectbox("Streaming Movies", ["Pilih...", "Yes", "No", "No internet service"])
        Contract = st.selectbox("Contract", ["Pilih...", "Month-to-month", "One year", "Two year"])
        PaperlessBilling = st.selectbox("Paperless Billing", ["Pilih...", "Yes", "No"])
        PaymentMethod = st.selectbox("Payment Method", ["Pilih...", "Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"])
        MonthlyCharges = st.number_input("Monthly Charges", min_value=0.0, max_value=1000.0, step=0.1, value=0.0)
        TotalCharges = st.number_input("Total Charges", min_value=0.0, max_value=10000.0, step=0.1, value=0.0)

    # Validasi input sebelum prediksi
    if st.button("Prediksi"):
        if (
            "Pilih..." in [gender, SeniorCitizen, Partner, Dependents, PhoneService, MultipleLines, InternetService, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies, Contract, PaperlessBilling, PaymentMethod]
        ):
            st.error("Harap isi semua kolom sebelum melakukan prediksi!")
        else:
            input_data = pd.DataFrame({
                "gender": [1 if gender == "Male" else 0],
                "SeniorCitizen": [1 if SeniorCitizen == "Yes" else 0],
                "Partner": [1 if Partner == "Yes" else 0],
                "Dependents": [1 if Dependents == "Yes" else 0],
                "tenure": [tenure],
                "PhoneService": [1 if PhoneService == "Yes" else 0],
                "MultipleLines": [0 if MultipleLines == "No" else 1 if MultipleLines == "Yes" else 2],
                "InternetService": [0 if InternetService == "No" else 1 if InternetService == "DSL" else 2],
                "OnlineSecurity": [0 if OnlineSecurity == "No" else 1 if OnlineSecurity == "Yes" else 2],
                "OnlineBackup": [0 if OnlineBackup == "No" else 1 if OnlineBackup == "Yes" else 2],
                "DeviceProtection": [0 if DeviceProtection == "No" else 1 if DeviceProtection == "Yes" else 2],
                "TechSupport": [0 if TechSupport == "No" else 1 if TechSupport == "Yes" else 2],
                "StreamingTV": [0 if StreamingTV == "No" else 1 if StreamingTV == "Yes" else 2],
                "StreamingMovies": [0 if StreamingMovies == "No" else 1 if StreamingMovies == "Yes" else 2],
                "Contract": [0 if Contract == "Month-to-month" else 1 if Contract == "One year" else 2],
                "PaperlessBilling": [1 if PaperlessBilling == "Yes" else 0],
                "PaymentMethod": [
                    0 if PaymentMethod == "Electronic check" else
                    1 if PaymentMethod == "Mailed check" else
                    2 if PaymentMethod == "Bank transfer (automatic)" else 3
                ],
                "MonthlyCharges": [MonthlyCharges],
                "TotalCharges": [TotalCharges]
            })

            # Lakukan prediksi
            prediction = model.predict(input_data)[0]
            probability = model.predict_proba(input_data)[0]

            if prediction == 1:
                st.warning(f"Pelanggan kemungkinan akan churn. Probabilitas: {probability[1]:.2f}")
            else:
                st.success(f"Pelanggan kemungkinan tidak akan churn. Probabilitas: {probability[0]:.2f}")


elif menu == "Akurasi":
    st.title("Akurasi Model")
    st.write("Berikut adalah perbandingan akurasi dari berbagai metode yang digunakan:")

    # CSS untuk memperbaiki tampilan tabel
    st.markdown("""
        <style>
        table {
            color: white;
            background-color: #112233;
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            border: 1px solid white;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #223344;
        }
        </style>
    """, unsafe_allow_html=True)

    # Data untuk tabel akurasi
    accuracy_data = {
        "Metode": [
            "Random Forest",
            "Random Forest + ROS",
            "Random Forest + SMOTE",
            "Random Forest + PCA",
            "Random Forest + PCA + ROS",
            "Random Forest + PCA + SMOTE"
        ],
        "Akurasi": [
            "77.39%",
            "87.94%",
            "83.34%",
            "73.13%",
            "88.23%",
            "80.78%"
        ]
    }

    # Tampilkan tabel sebagai HTML
    st.markdown(pd.DataFrame(accuracy_data).to_html(index=False), unsafe_allow_html=True)

if menu == "Dataset":
    st.title("Dataset")
    st.write("Dataset yang digunakan dalam model ini:")
    try:
        df = pd.read_csv(data_path)
        st.dataframe(df)
    except FileNotFoundError:
        st.error("File dataset tidak ditemukan.")

elif menu == "Tentang Sistem":
    st.title("Tentang Sistem")
    st.write("""
    Sistem ini dibuat sebagai alat uji dari skripsi yang disusun oleh **Rifa Adinta Farda (4611419050)**  
    Dalam sistem ini, terdapat beberapa menu yang ditampilkan yaitu, **prediksi**, **dataset**, **akurasi**,  dan **tentang sistem**. yang dijelaskan sebagai berikut.
    """)

    # Gunakan CSS untuk mempercantik tampilan
    st.markdown("""
    <style>
        .card {
            background-color: #1e3a8a; 
            color: white; 
            border-radius: 10px; 
            padding: 20px; 
            margin: 10px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
        }
        .card h3 {
            color: #fbbf24; 
            margin-bottom: 10px;
        }
        .icon {
            font-size: 20px; 
            margin-right: 10px;
            color: #fbbf24;
        }
    </style>
    """, unsafe_allow_html=True)

    # Membuat layout dua kolom
    col1, col2 = st.columns(2)

    # Kolom pertama
    with col1:
        st.markdown("""
        <div class="card">
            <h3><span class="icon">🔮</span>Prediksi</h3>
            <p>Menu prediksi merupakan halaman untuk melakukan prediksi customer churn, pada halaman ini pengguna wajib melakukan input data untuk mengetahui hasil prediksi.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <h3><span class="icon">📊</span>Akurasi</h3>
            <p>Menu akurasi berfungsi untuk menampilkan hasil akurasi pengujian dari semua metode yang digunakan dalam penelitian ini.</p>
        </div>
        """, unsafe_allow_html=True)

    # Kolom kedua
    with col2:
        st.markdown("""
        <div class="card">
            <h3><span class="icon">📂</span>Dataset</h3>
            <p>Menu dataset menunjukkan dataset yang dipakai pada penelitian ini yang telah melalui proses pembersihan dan resampling serta memperoleh akurasi terbaik</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <h3><span class="icon">✅</span>Tentang Sistem</h3>
            <p>Menu tentang sistem berisi penjelasan secara umum mengenai menu yang terdapat pada sistem.</p>
        </div>
        """, unsafe_allow_html=True)