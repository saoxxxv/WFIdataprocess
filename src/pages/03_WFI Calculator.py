import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__),"../.."))
import io

from libs.libWFI import add_WERs, calc_WFI


st.title("WFI Calculator")
st.markdown("""
    Adds calculated WFI parameters to a Excel file containing experimental and simulation data.""")

with st.expander("Terms and Conditions"):
    st.markdown("""
    * **For non-commercial use:** free to use with appropriate citation.              
    Cite this:  
    Orito, Y. &ensp;_ACS Omega_ **2025**, _10_ (9), 9266–9274. https://doi.org/10.1021/acsomega.4c09609.  
    * **For commercial use:** please contact the author.
                    
    See also the [Github repository](https://github.com/saoxxxv/WFIdataprocess).
                """)

uploaded_file = st.sidebar.file_uploader("Upload an Excel file", type=["xlsx"])
if uploaded_file is not None:
    st.sidebar.header("WFI Parameters")
    WER_a = st.sidebar.number_input("WER_a", value=1.0)
    WER_b = st.sidebar.number_input("WER_b", value=-9.0)
    WER_k = st.sidebar.number_input("WER_k", value=-10.0)

    if st.button("Process"):
        # Read all sheets from the uploaded Excel file
        xls = pd.ExcelFile(uploaded_file)
        sheet_names = xls.sheet_names
        # st.sidebar.header("Select Sheet")
        # sheet_name = st.sidebar.selectbox("Sheet Name", options=sheet_names, index=0)

        processed_sheets = {}
        for sheet_name in sheet_names:
            df_trimmed = add_WERs(uploaded_file, sheet_name, WER_a, WER_b, WER_k)
            
            # Error handling.
            if df_trimmed is None or df_trimmed.empty:
                st.error(f"The processed data for sheet '{sheet_name}' is empty or invalid. Please check the input file.")
                continue
            
            df_calcd = calc_WFI(df_trimmed, WER_a, WER_b, WER_k)

            processed_sheets[sheet_name] = df_calcd
        
        # Write processed data to a temporary Excel file on the memory
        output_stream = io.BytesIO()
        with pd.ExcelWriter(output_stream, engine='openpyxl') as writer:
            for sheet_name, df in processed_sheets.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        output_stream.seek(0)

        st.success("WFI parameters added successfully. You can download the processed file below.")

        # Write processed data to a new Excel file
        output_file = os.path.splitext(uploaded_file.name)[0] + "_WFI_added.xlsx"
        st.download_button(
            label="Download Processed Excel File",
            data=output_stream,
            file_name=output_file,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
