from flask import Flask, request, jsonify
from celery import Celery
from pydantic import BaseModel, ValidationError, validator
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from xml.etree import ElementTree as ET
from celery.result import AsyncResult

app = Flask(__name__)

# Конфигурация для SQLAlchemy
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://admin:123@localhost:5432/main_db'
engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Модель для SQLAlchemy
class Entity(Base):
    __tablename__ = 'entities'
    id = Column(Integer, primary_key=True)
    data = Column(String)

    def __repr__(self):
        return f"<Entity(id={self.id}, data='{self.data}')>"

Base.metadata.create_all(engine)

# Pydantic модели для валидации
class JsonRequest(BaseModel):
    data: dict

class XmlRequest(BaseModel):
    data: str

    @validator('data')
    def validate_xml(cls, value):
        try:
            ET.fromstring(value)
        except ET.ParseError as e:
            raise ValueError(f"Invalid XML: {e}")
        return value

# Конфигурация для Celery
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Задача Celery для конвертации
@celery.task
def convert_and_save(data, direction):
    if direction == 'json_to_xml':
        root = ET.Element("root")
        for key, value in data.items():
            ET.SubElement(root, key).text = str(value)
        xml_data = ET.tostring(root).decode()
        return xml_data
    elif direction == 'xml_to_json':
        root = ET.fromstring(data)
        json_data = {elem.tag: elem.text for elem in root}
        return json_data
    return None

# Эндпоинты Flask
@app.route('/json_to_xml', methods=['POST'])
def json_to_xml():
    try:
        request_data = JsonRequest.parse_raw(request.data)
        task = convert_and_save.delay(request_data.data, 'json_to_xml')
        result = task.wait()
        with Session() as session:
            entity = Entity(data=str(request_data.data))
            session.add(entity)
            session.commit()
        return jsonify({'result': result})
    except ValidationError as e:
        return jsonify({'error': e.errors()}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/xml_to_json', methods=['POST'])
def xml_to_json():
    try:
        xml_string = request.data.decode()
        request_data = XmlRequest(data=xml_string)
        task = convert_and_save.delay(request_data.data, 'xml_to_json')
        result = task.wait()
        with Session() as session:
            entity = Entity(data=request_data.data)
            session.add(entity)
            session.commit()
        return jsonify({'result': result})
    except ValidationError as e:
        return jsonify({'error': e.errors()}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/task_status/<task_id>')
def task_status(task_id):
    task = AsyncResult(task_id, app=celery)
    return jsonify({'status': task.status, 'result': task.result})

if __name__ == '__main__':
    app.run(debug=True)
