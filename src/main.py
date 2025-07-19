import streamlit as st

st.set_page_config(
    page_title="WFI Data Processor",
    page_icon=":bar_chart:",
    layout="wide"
)

st.title("Weighted Fitting Index (WFI) Data Processing")

with st.expander("Terms and Conditions"):
    st.markdown("""
    * **For non-commercial use:** free to use with appropriate citation.              
    Cite this:  
    Orito, Y. &ensp;_ACS Omega_ **2025**, _10_ (9), 9266–9274. https://doi.org/10.1021/acsomega.4c09609.  
    * **For commercial use:** please contact the author.
                """)
    
st.markdown("""
## Please select a page for each function from the sidebar.
  
  
Copyright © 2025 Yuya Orito. All rights reserved.
""")
