from celery import Celery
from config import Config
from xml.etree import ElementTree as ET

celery = Celery('tasks', broker=Config.CELERY_BROKER_URL)
celery.conf.update(result_backend=Config.CELERY_RESULT_BACKEND)

@celery.task
def convert_and_save(data, direction):
    if direction == 'json_to_xml':
        root = ET.Element("data")
        for key, value in data.items():
            ET.SubElement(root, key).text = str(value)
        xml_data = ET.tostring(root).decode()
        return xml_data
    elif direction == 'xml_to_json':
        root = ET.fromstring(data)
        json_data = {elem.tag: elem.text for elem in root}
        return json_data
    return None
