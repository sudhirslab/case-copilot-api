python3 -m venv .venv
source $(pwd)/.venv/bin/activate
python3 -m pip install -r requirements.txt
pip install --upgrade pip
uvicorn main:app --reload

