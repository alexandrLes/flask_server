from pydantic import BaseModel, validator
from xml.etree import ElementTree as ET

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
