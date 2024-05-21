import unittest
import json
from flask_testing import TestCase
from app import app
from models import Session, Entity, Base, engine
from config import TestConfig

class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object(TestConfig)
        return app

    def setUp(self):
        Base.metadata.create_all(engine)

    def tearDown(self):
        Base.metadata.drop_all(engine)

class TestConversionTasks(BaseTestCase):
    def test_json_to_xml_conversion(self):
        with open('App_info.json', 'w') as f:
            json.dump({"name": "John", "age": 30}, f)

        with open('App_info.json', 'rb') as f:
            response = self.client.post('/json_to_xml', content_type='multipart/form-data', data={'file': f})
        self.assertEqual(response.status_code, 200)
        self.assertIn('<name>John</name>', response.json['result'])
        self.assertIn('<age>30</age>', response.json['result'])
        
        with Session() as session:
            entity = session.query(Entity).first()
            self.assertEqual(entity.name, 'John')
            self.assertEqual(entity.age, 30)

    def test_xml_to_json_conversion(self):
        xml_data = """
        <data>
            <name>John</name>
            <age>30</age>
        </data>
        """
        with open('App_info.xml', 'w') as f:
            f.write(xml_data)

        with open('App_info.xml', 'rb') as f:
            response = self.client.post('/xml_to_json', content_type='multipart/form-data', data={'file': f})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['result']['name'], 'John')
        self.assertEqual(response.json['result']['age'], '30')

        with Session() as session:
            entity = session.query(Entity).first()
            self.assertEqual(entity.name, 'John')
            self.assertEqual(entity.age, 30)

    def test_invalid_xml(self):
        invalid_xml_data = "<data><name>John</name><age>30</age>"
        with open('Invalid.xml', 'w') as f:
            f.write(invalid_xml_data)

        with open('Invalid.xml', 'rb') as f:
            response = self.client.post('/xml_to_json', content_type='multipart/form-data', data={'file': f})
        self.assertEqual(response.status_code, 400)
        self.assertIsInstance(response.json, dict)

if __name__ == '__main__':
    unittest.main()
