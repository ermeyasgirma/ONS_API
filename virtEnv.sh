#python3 -m venv .ONSvenv
#source .ONSvenv/bin/activate
#pip freeze > requirements.txt
#pip install flask
#pip install pandas
#pip install openpyxl
export FLASK_APP=api.py
export FLASK_ENC=development
flask run
