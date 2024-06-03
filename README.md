# Flask Server

This is a Flask server that performs data conversion between JSON and XML formats using Celery for asynchronous task processing and SQLAlchemy for interacting with the PostgreSQL database.

## Installation

**1.** Clone the repository to your local machine:

```git clone git@github.com:alexandrLes/flask_server.git```

**2.** Install the dependencies:

```pip install -r requirements.txt```

**3.** Set up and configure PostgreSQL and Redis servers.

## Configuration

**1.** Create / edit a configuration file `config.py` and specify the connection parameters to your PostgreSQL and Redis servers.

```python
# config.py

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://admin:123@localhost:5432/main_db'
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    TESTING = False
```
## Running 
```shell
redis-server
celery -A tasks worker --loglevel=info
python app.py
```
## Endpoints
## Testing
```shell
python test_requests.py
```
