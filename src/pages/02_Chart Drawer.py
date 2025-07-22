import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__),"../.."))

from libs.libWFI import add_WERs, draw_WERcharts


st.title("Chart drawer with Weighted Error Ranges (WER)")

with st.expander("Terms and Conditions"):
    st.markdown("""
    * **For non-commercial use:** free to use with appropriate citation.              
    Cite this:  
    Orito, Y. &ensp;_ACS Omega_ **2025**, _10_ (9), 9266–9274. https://doi.org/10.1021/acsomega.4c09609.  
    * **For commercial use:** please contact the author.
                """)

uploaded_file = st.sidebar.file_uploader("Upload an Excel file", type=["xlsx"])
if uploaded_file is not None:
    sheet_name = st.sidebar.number_input("Sheet index No", value=0)
    st.sidebar.header("WFI Parameters")
    WER_a = st.sidebar.number_input("WER_a", value=1.0)
    WER_b = st.sidebar.number_input("WER_b", value=-9.0)
    WER_k = st.sidebar.number_input("WER_k", value=-10.0)
    st.sidebar.header("Chart drawing settings")
    var_marker_size = st.sidebar.number_input("Marker Size", value=5)
    var_font_size = st.sidebar.number_input("Font Size", value=10)
    var_chart_size_inches_width = st.sidebar.number_input("Chart Width (inches)", value=3)
    flagShowLegend = st.sidebar.checkbox("Show Legend", value=True)
    colour_preset_indices = {0: "A", 4: "B", 8: "C"}
    sim_startcolour = st.sidebar.selectbox("Simulation Start Color Preset", options=list(colour_preset_indices.keys()), index=0, format_func=lambda x: colour_preset_indices[x])
    exp_startcolour = st.sidebar.selectbox("Experiment Start Color Preset", options=list(colour_preset_indices.keys()), index=0, format_func=lambda x: colour_preset_indices[x])

    if st.button("Process"):
    
        df_trimmed = add_WERs(uploaded_file, sheet_name, WER_a, WER_b, WER_k)
        
        # Error handling.
        if df_trimmed is None or df_trimmed.empty:
            st.error("The processed data is empty or invalid. Please check the input file.")
            st.stop()
    
        fig, ax = draw_WERcharts(
            df_trimmed, 
            var_marker_size, 
            var_font_size, 
            var_chart_size_inches_width, 
            flagShowLegend, 
            sim_startcolour, 
            exp_startcolour
        )

        st.pyplot(fig)