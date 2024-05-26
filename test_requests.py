import requests
import json

# URL вашего запущенного Flask-приложения
BASE_URL = 'http://localhost:5000'

def test_json_to_xml():
    url = f"{BASE_URL}/json_to_xml"
    headers = {'Content-Type': 'multipart/form-data'}

    # Пример данных для JSON
    json_data = {
        "id": 1,
        "user_id": 3878,
        "first_name": "Максим",
        "second_name": "Яруллин",
        "middle_name": None,
        "dict_sex_id": 1,
        "birthday": "2005-08-07",
        "citizenship_id": 185,
        "motherland": "Россия Г.Астана",
        "email": "mail@etu.ru",
        "tel_mobile": "+7 (888) 888-88-88",
        "address_txt1": "Могилевская область",
        "address_txt2": None,
        "address_txt3": None,
        "address_txt4": None,
        "has_another_living_address": False,
        "second_address_txt1": None,
        "second_address_txt2": None,
        "second_address_txt3": None,
        "second_address_txt4": None,
        "passport_type_id": 1,
        "passport_series": "5661",
        "passport_number": "111111",
        "passport_begda": "2019-09-08",
        "passport_endda": None,
        "passport_org_code": "111-111",
        "passport_issued_by": "МВД-АВОР.ПРДЛПАРОДАЬЕК",
        "need_hostel": None,
        "special_conditions": None,
        "is_with_disabilities": None,
        "diploma_series": "123132",
        "diploma_number": "1211221",
        "diploma_date": "2000-10-10",
        "diploma_registration_number": "уц",
        "graduated_university_text": "кцу",
        "edu_diploma_name_text": None,
        "snils": None,
        "revision": 1,
        "passport_name_text": None,
        "has_original_edu_diploma": False,
        "passport_uuid": "151ad3fc-756f-46d0-8ec0-9d0355ec693a",
        "public_code": "870-074-745 12"
    }

    # Запись JSON в файл
    with open('App_info.json', 'w') as json_file:
        json.dump(json_data, json_file)

    # Отправка POST-запроса с файлом JSON
    with open('App_info.json', 'rb') as json_file:
        response = requests.post(url, files={'file': json_file})

    print("test_json_to_xml Response:")
    print(response.status_code)
    print(response.json())

def test_xml_to_json():
    url = f"{BASE_URL}/xml_to_json"
    headers = {'Content-Type': 'multipart/form-data'}

    # Пример данных для XML
    xml_data = '''
    <root>
        <id>2</id>
        <user_id>3878</user_id>
        <first_name>Максим</first_name>
        <second_name>Яруллин</second_name>
        <middle_name></middle_name>
        <dict_sex_id>1</dict_sex_id>
        <birthday>2005-08-07</birthday>
        <citizenship_id>185</citizenship_id>
        <motherland>Россия Г.Астана</motherland>
        <email>mail@etu.ru</email>
        <tel_mobile>+7 (888) 888-88-88</tel_mobile>
        <address_txt1>Могилевская область</address_txt1>
        <address_txt2></address_txt2>
        <address_txt3></address_txt3>
        <address_txt4></address_txt4>
        <has_another_living_address>False</has_another_living_address>
        <second_address_txt1></second_address_txt1>
        <second_address_txt2></second_address_txt2>
        <second_address_txt3></second_address_txt3>
        <second_address_txt4></second_address_txt4>
        <passport_type_id>1</passport_type_id>
        <passport_series>5661</passport_series>
        <passport_number>111111</passport_number>
        <passport_begda>2019-09-08</passport_begda>
        <passport_endda></passport_endda>
        <passport_org_code>111-111</passport_org_code>
        <passport_issued_by>МВД-АВОР.ПРДЛПАРОДАЬЕК</passport_issued_by>
        <need_hostel></need_hostel>
        <special_conditions></special_conditions>
        <is_with_disabilities></is_with_disabilities>
        <diploma_series>123132</diploma_series>
        <diploma_number>1211221</diploma_number>
        <diploma_date>2000-10-10</diplома_date>
        <diploma_registration_number>уц</diplома_registration_number>
        <graduated_university_text>кцу</graduated_university_text>
        <edu_diploma_name_text></edu_diplома_name_text>
        <snils></snils>
        <revision>1</revision>
        <passport_name_text></passport_name_text>
        <has_original_edu_diploma>False</has_original_edu_dиплома>
        <passport_uuid>151ad3fc-756f-46d0-8ec0-9d0355ec693a</passport_uuid>
        <public_code>870-074-745 12</public_code>
    </root>
    '''

    # Запись XML в файл
    with open('App_info.xml', 'w') as xml_file:
        xml_file.write(xml_data)

    # Отправка POST-запроса с файлом XML
    with open('App_info.xml', 'rb') as xml_file:
        response = requests.post(url, files={'file': xml_file})

    print("test_xml_to_json Response:")
    print(response.status_code)
    print(response.json())

if __name__ == '__main__':
    test_json_to_xml()
    test_xml_to_json()
