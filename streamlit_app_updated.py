import streamlit as st
import pandas as pd
import joblib

# ✅ Confirm secrets are loaded, but don't display them
st.title("Exporter Classifier App")
st.success("✅ OAuth secrets loaded successfully.")

# ⬇️ --- Existing app functionality starts here --- ⬇️

st.header("Upload Exporter List")

uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    if "exporter_name" not in df.columns:
        st.error("❌ Please include a column named 'exporter_name' in your file.")
    else:
        # Load ML model and vectorizer
        model = joblib.load("exporter_classifier_model.pkl")
        vectorizer = joblib.load("tfidf_vectorizer.pkl")

        # Predict exporter type
        exporter_names = df["exporter_name"].astype(str)
        X = vectorizer.transform(exporter_names)
        predictions = model.predict(X)

        df["Predicted Type"] = predictions
        st.success("✅ Classification complete!")
        st.dataframe(df)

        # Download button
        st.download_button(
            label="📥 Download Results",
            data=df.to_excel(index=False, engine="openpyxl"),
            file_name="classified_exporters.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# 🔚 End of app
