import streamlit as st

st.title("How to use")
st.markdown("""
## Chart Drawer
Draw charts with Weighted Error Ranges (WER) from an Excel file containing experimental and simulation data.

### Excel data format
The Excel file shuld have the following structure:
- The first row should contain the column headers.
- The columns with "Time" or "Sim" or "Exp" in the second row are processed.
    - "Time" for time series, currently only one time series is supported.
    - "Sim" for simulation data. WERs are calculated from this data.
    - "Exp" for experimental data. 
    - The colours are assigned based on the order of the columns (left to right). 
    Make sure the columns are sorted in same order for both "Sim" and "Exp". 
- The third row is reserved for output data, which will be used in WFI calculator.
- The fourth row and below are for the actual data values.

1. Upload your Excel file using the sidebar.
2. Specify the sheet index number to read data from.
3. Adjust the WER parameters and chart settings as needed.
4. Click the "Process" button to generate the chart.

""")
