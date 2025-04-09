import streamlit as st
import pandas as pd
import joblib
from io import BytesIO

# Load model and vectorizer
model = joblib.load("exporter_classifier_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

st.set_page_config(page_title="Exporter Classification App", page_icon="📦")
st.title("📦 Exporter Classification App")
st.write("Upload an Excel file containing exporter information to classify exporter types.")

uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

if uploaded_file:
    try:
        # Read the Excel file
        df = pd.read_excel(uploaded_file)

        # Standardize column names
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

        # Check for required columns
        if "exporter_name" not in df.columns:
            st.error("The file must contain at least a column named 'exporter_name'.")
        else:
            # Combine relevant text columns
            text_data = df["exporter_name"].astype(str)

            if "exporter_add" in df.columns:
                text_data += " " + df["exporter_add"].astype(str)
            if "exporter_city" in df.columns:
                text_data += " " + df["exporter_city"].astype(str)

            # Transform text and predict
            X = vectorizer.transform(text_data)
            predictions = model.predict(X)

            # Create result dataframe
            result_df = df[["exporter_name"]].copy()
            result_df["Predicted Exporter Type"] = predictions

            st.success("Classification complete!")
            st.dataframe(result_df.head(10))

            # Create downloadable Excel
            output = BytesIO()
            result_df.to_excel(output, index=False, engine='openpyxl')
            output.seek(0)
            st.download_button(
                label="📥 Download Full Results",
                data=output,
                file_name="classified_exporters.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"Error processing file: {e}")
