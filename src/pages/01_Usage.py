import streamlit as st
import base64

st.title("How to use")

st.markdown("""
## Input Excel data format
The Excel file shuld have the following structure:
- The first row should contain the column headers.
    - The text is used as the series name in the legend.
    - TeX formatting is supported, e.g., `\\Delta` for delta.
- The columns with "Time", "Sim" or "Exp" in the second row are processed.
    - "Time" for time series, in min. Currently only one time series is supported.
    - "Sim" for simulation data. WERs are calculated from this data. Plotted as a line with shaded error range.
    - "Exp" for experimental data. Plotted without line.
    - The colours are assigned based on the order of the columns (left to right). 
    Make sure the columns are sorted in same order for both "Sim" and "Exp". 
- The third row is reserved for output data, which will be used in WFI calculator.
- The fourth row and below are for the actual data values in %.

""")

with open("assets/sample_data.xlsx", "rb") as file:
    sample_data = file.read()
    b64 = base64.b64encode(sample_data).decode()
    href = f'<a href="data:file/xlsx;base64,{b64}" download="sample_data.xlsx">Download Sample Data</a>: \
            A part of the SI of: Orito, Y. _Org. Process Res. Dev._ **2025**, _29_ (7), 1757–1765. https://doi.org/10.1021/acs.oprd.5c00107.'
    st.markdown(href, unsafe_allow_html=True)

st.markdown("""
## Chart Drawer
Draws chart with Weighted Error Ranges (WER) from an Excel file containing experimental and simulation data.


1. Upload your Excel file using the sidebar.
2. Specify the sheet index number to read data from.
3. Adjust the WER parameters and chart settings as needed.
4. Click the "Process" button to generate the chart.


## WFI Calculator
Creates a new Excel file with calculated WFI parameters added to the original data.


1. Upload your Excel file using the sidebar.
2. Adjust the WER parameters as needed.
3. Click the "Process" button to generate the new Excel file with WFI parameters.
4. Download the processed file.

""")

