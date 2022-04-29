# garrett

# Setup and running

```
python -m virtualenv venv
source venv/bin/activate
pip install -r requirements
python manage.py makemigrations
python manage.py runserver
curl http://localhost:8000/api/user/me
```
