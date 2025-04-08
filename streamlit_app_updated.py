import streamlit as st
import pandas as pd
import joblib
import os
import re

# Load the model and vectorizer
model = joblib.load("exporter_classifier_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

def clean_text(text):
    if pd.isna(text):
        return ""
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text.lower()

def preprocess_dataframe(df):
    # Standardize column names
    df.columns = df.columns.str.strip().str.lower()

    # Rename likely variants
    rename_map = {
        'exporter name': 'exporter_name',
        'exporter_add': 'exporter_add',
        'exporter city': 'exporter_city',
    }
    df = df.rename(columns={col: rename_map[col] for col in df.columns if col in rename_map})

    # Fill missing columns
    for col in ['exporter_name', 'exporter_add', 'exporter_city']:
        if col not in df.columns:
            df[col] = ""

    # Fill missing values and clean
    for col in ['exporter_name', 'exporter_add', 'exporter_city']:
        df[col] = df[col].fillna("").apply(clean_text)

    # Create combined column
    df['combined_text'] = df['exporter_name'] + " " + df['exporter_add'] + " " + df['exporter_city']
    return df

def predict(df):
    X = vectorizer.transform(df['combined_text'])
    preds = model.predict(X)
    df['Predicted Exporter Type'] = ['Exporter' if p == 1 else 'Manufacturer' for p in preds]
    return df[['exporter_name', 'Predicted Exporter Type']]

# Streamlit App
st.set_page_config(page_title="Exporter Classifier App", layout="centered")
st.title("📦 Exporter Classification App")

uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        df = preprocess_dataframe(df)
        result_df = predict(df)

        st.success("Classification complete!")
        st.dataframe(result_df)

        # Download button
        result_xlsx = result_df.to_excel(index=False)
        st.download_button(
            label="⬇️ Download Full Results",
            data=result_xlsx,
            file_name="classified_exporters.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.info("Please upload an Excel file with at least the 'exporter_name' column.")
