# flask_server

1. pip install -r requirements.txt
2. service postgresql start
3. celery -A celery_worker.celery worker --loglevel=info
4. python app.py