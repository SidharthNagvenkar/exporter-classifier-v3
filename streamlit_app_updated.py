import streamlit as st
import pandas as pd
import joblib
import os

# Load model and vectorizer
model = joblib.load("exporter_classifier_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

st.set_page_config(page_title="Exporter Classifier", layout="centered")

st.title("🌍 Exporter Category Classifier")
st.write("Upload an Excel file with exporter information to predict categories.")

uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)

        # Check for required columns
        possible_cols = ['exporter_name', 'exporter_add', 'exporter_city']
        available_cols = [col for col in possible_cols if col in df.columns]

        if not available_cols:
            st.error("❌ The file must contain at least the column 'exporter_name'.")
        else:
            # Combine the available text columns
            df['combined_text'] = df[available_cols].fillna('').astype(str).agg(' '.join, axis=1)

            # Vectorize the input
            X = vectorizer.transform(df['combined_text'])

            # Make predictions
            preds = model.predict(X)

            # Convert labels to readable format (0 → Merchant, 1 → Manufacturer)
            readable_preds = ['Merchant Exporter' if p == 0 else 'Manufacturer' for p in preds]
            df['Predicted Exporter Type'] = readable_preds

            st.success("✅ Classification complete! Preview below:")
            st.dataframe(df[['Predicted Exporter Type'] + available_cols].head())

            # Download result
            output_filename = "classified_exporters.xlsx"
            df.to_excel(output_filename, index=False)

            with open(output_filename, "rb") as f:
                st.download_button(
                    label="📥 Download Results as Excel",
                    data=f,
                    file_name=output_filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

    except Exception as e:
        st.error(f"⚠️ Error processing file: {e}")
