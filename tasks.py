from celery import Celery
from config import Config
import dicttoxml
import xmltodict
from models import Session, Entity
from pydantic import BaseModel, ValidationError

celery = Celery('tasks', broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_RESULT_BACKEND)

class EntityModel(BaseModel):
    id: int
    user_id: int
    first_name: str
    second_name: str
    middle_name: str | None = None
    dict_sex_id: int
    birthday: str
    citizenship_id: int
    motherland: str
    email: str
    tel_mobile: str
    address_txt1: str
    address_txt2: str | None = None
    address_txt3: str | None = None
    address_txt4: str | None = None
    has_another_living_address: bool
    second_address_txt1: str | None = None
    second_address_txt2: str | None = None
    second_address_txt3: str | None = None
    second_address_txt4: str | None = None
    passport_type_id: int
    passport_series: str
    passport_number: str
    passport_begda: str
    passport_endda: str | None = None
    passport_org_code: str
    passport_issued_by: str
    need_hostel: bool | None = None
    special_conditions: str | None = None
    is_with_disabilities: bool | None = None
    diploma_series: str
    diploma_number: str
    diploma_date: str
    diploma_registration_number: str
    graduated_university_text: str
    edu_diploma_name_text: str | None = None
    snils: str | None = None
    revision: int
    passport_name_text: str | None = None
    has_original_edu_diploma: bool
    passport_uuid: str
    public_code: str

@celery.task
def convert_and_save(data, conversion_type):
    session = Session()
    try:
        if conversion_type == 'json_to_xml':
            entity_data = EntityModel(**data)
            entity = Entity(**entity_data.dict())
            session.add(entity)
            session.commit()
            xml_data = dicttoxml.dicttoxml(entity_data.dict())
            return xml_data.decode()
        elif conversion_type == 'xml_to_json':
            json_data = xmltodict.parse(data)
            entity_data = EntityModel(**json_data['root'])
            entity = Entity(**entity_data.dict())
            session.add(entity)
            session.commit()
            return json_data['root']
    except ValidationError as e:
        session.rollback()
        return {'error': str(e)}
    finally:
        session.close()
