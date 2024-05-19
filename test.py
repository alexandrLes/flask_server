import requests

# Пример отправки JSON для конвертации в XML
json_data = {
    "data": {
        "name": "John",
        "age": 30
    }
}

response = requests.post('http://127.0.0.1:5000/json_to_xml', json=json_data)
try:
    print("JSON to XML response:", response.json())
except requests.exceptions.JSONDecodeError:
    print("Response content:", response.content)

# Пример отправки XML для конвертации в JSON
xml_data = """
<data>
    <name>John</name>
    <age>30</age>
</data>
"""

response = requests.post('http://127.0.0.1:5000/xml_to_json', data=xml_data, headers={'Content-Type': 'application/xml'})
try:
    print("XML to JSON response:", response.json())
except requests.exceptions.JSONDecodeError:
    print("Response content:", response.content)
