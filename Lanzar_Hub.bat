@echo off
echo Iniciando Video Intelligence Hub...
set PYTHONPATH=.
call venv\Scripts\activate
streamlit run app/main.py
pause
