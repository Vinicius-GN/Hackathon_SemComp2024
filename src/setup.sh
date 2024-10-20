python3 -m venv .
source $(pwd)/bin/activate
pip install -r requirements.txt
python bot/app.py & python Site/manage.py runserver