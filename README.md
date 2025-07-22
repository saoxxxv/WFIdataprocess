# WFI data processor
A data processor for chemical reaction timecourses which provides weighted error range / fitting indices calculations and interactive chart drawing.

## Purpose
This tool has been developed as a part of research work regarding mechanism-oriented kinetic analyls of chemical reactions to help organic chemists 
visualizing the relationship between simulation and experimental results, thereby to allow investigating extrapolability of the reaction kinetic model.  
It is specially designed to support synthetic organic chemists who are not quite familiar with analyzing reaction mechanisms through physical calculations 
rather than utilizing curly arrows and dots, by encupsulation of mathematical flavour and automatic processing of user-friendly Excel data.

## Output samples
![Screenshot](./assets/sample_chart.png)

## Installation
If you have python environment in your local, try
```bash
git clone https://github.com/saoxxxv/WFIdataprocess.git
cd WFIdataprocess
pip install -r requirements.txt
streamlit run src/Top.py
```
Or, simply access web app ran on Streamlit cloud

```
Currently under construction
```

## Usage
See Usage page shown in sidebar for input data format etc.

## License
This project is dual-licensed:  
- **AGPLv3** for academic and non-commercial use.  
- **Commercial licenses** are available upon request.  

## Citation
Cite this work as:  
Orito, Y.  _ACS Omega_ **2025**, _10_, 9266–9274. https://doi.org/10.1021/acsomega.4c09609.

## Contact
For bug reports, feature requests, or commercial inquiries, please contact:  
Yuya Orito  
[saoxxxv@gmail.com]
