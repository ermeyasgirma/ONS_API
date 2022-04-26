#python3 -m venv .ONSvenv
#source .ONSvenv/bin/activate
#pip freeze > requirements.txt
#pip install flask

export FLASK_APP=api.py
export FLASK_ENC=development
flask run
