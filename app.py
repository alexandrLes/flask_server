from flask import Flask, request, jsonify
from config import Config
from models import Session, Entity
from schemas import JsonRequest, XmlRequest
from tasks import celery
from pydantic import ValidationError
from celery.result import AsyncResult
import json
import xml.etree.ElementTree as ET

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/json_to_xml', methods=['POST'])
def json_to_xml():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if file and file.filename.endswith('.json'):
            request_data = json.load(file)
            try:
                validated_data = JsonRequest(**request_data)
            except ValidationError as e:
                return jsonify({'error': e.errors()}), 400

            task = celery.send_task('tasks.convert_and_save', args=[request_data, 'json_to_xml'])
            result = task.wait()
            with Session() as session:
                entity = Entity(**request_data)
                session.add(entity)
                session.commit()
            return jsonify({'result': result})
        else:
            return jsonify({'error': 'Unsupported file type'}), 400
    except ValidationError as e:
        return jsonify({'error': e.errors()}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/xml_to_json', methods=['POST'])
def xml_to_json():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if file and file.filename.endswith('.xml'):
            xml_string = file.read().decode()
            
            try:
                root = ET.fromstring(xml_string)
            except ET.ParseError as e:
                return jsonify({'error': 'Invalid XML: ' + str(e)}), 400
            
            request_data = {}
            task = celery.send_task('tasks.convert_and_save', args=[request_data, 'xml_to_json'])
            result = task.wait()
            
            with Session() as session:
                entity = Entity(name=result['name'], age=int(result['age']))
                session.add(entity)
                session.commit()
            
            return jsonify({'result': result})
        else:
            return jsonify({'error': 'Unsupported file type'}), 400
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
