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
    For simple data processing tools: Orito, Y. &nbsp;WFI Data Processor. _Zenodo_ **2025**. https://doi.org/10.5281/zenodo.16490790.  
    [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.16490790.svg)](https://doi.org/10.5281/zenodo.16490790)

    * **For commercial use:** please contact the author.
                    
    See also the [Github repository](https://github.com/saoxxxv/WFIdataprocess).
                """)

st.markdown("""
```math
WFI=\\frac{1}{n}\sum_{i=1}^{n}\\frac{E_{abs,i}}{E_{rel,i}\left(Y_{s,i}\\right)}
```

""")

st.warning("""
**Caution:**  
Chemists should be aware of choosing the appropriate data points of WFI(n) to 
calculate the WFI value based on deep chemical insights,
**especially when the reaction system develops in non-exponential manner.**
The data points after reaching plateau should be sparsely selected to avoid overfitting, whilst
the data points in the high-drift region should be densely selected to avoid underfitting.
Evenly spaced data points are recommended for linear region such as zeroth-order or semi-batch 
(dropwise) control.
**For more details, please refer to the original paper.**
""")

uploaded_file = st.sidebar.file_uploader("Upload an Excel file", type=["xlsx"])
if uploaded_file is not None:
    st.sidebar.header("WFI Parameters")
    WER_a = st.sidebar.number_input("WER_a", value=1.0)
    WER_b = st.sidebar.number_input("WER_b", value=-9.0)
    WER_k = st.sidebar.number_input("WER_k", value=-10.0)

    if st.button("Process"):
        try:
            # Read all sheets from the uploaded Excel file
            xls = pd.ExcelFile(uploaded_file)
            sheet_names = xls.sheet_names
        except Exception as e:
            st.error(f"Failed to open the uploaded Excel file. The file may be corrupted or not a valid Excel file. Details: {e}")
            st.stop()

        processed_sheets = {}
        for sheet_name in sheet_names:
            df_trimmed = add_WERs(uploaded_file, sheet_name, WER_a, WER_b, WER_k)
            
            # Error handling.
            if df_trimmed is None or df_trimmed.empty:
                st.error(f"The processed data for sheet '{sheet_name}' is empty or invalid. Please check the input file. (Maybe wrong simulation data?)")
                continue
            
            df_calcd = calc_WFI(df_trimmed, WER_a, WER_b, WER_k)

            if df_calcd is None or df_calcd.empty:
                st.error(f"Calculation of WFI for sheet '{sheet_name}' failed. Please check the input file. (Maybe wrong experimental data?)")
                continue

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
