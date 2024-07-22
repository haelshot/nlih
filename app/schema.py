from typing import Optional
import uuid
from ninja import Schema
from pydantic import Json
from datetime import datetime

class RegisterPatientSchema(Schema):
    email: str
    patient_name: str
    patient_firstname: str
    patient_lastname: str
    password: str


class RegisterDoctorSchema(Schema):
    email: str
    doctor_name: str
    doctor_firstname: str
    doctor_lastname: str
    password: str


class LoginSchema(Schema):
    email: str
    password: str


class ResponseSchema(Schema):
    is_ok: bool
    message: str
    payload: Optional[dict]
    err_data: Optional[str]

class SignInResponsePayload(Schema):
    user_id: str
    user_email: str
    access_token: str


class AppointmentSchema(Schema):
    datetime: datetime
    doctor_id: uuid.UUID
