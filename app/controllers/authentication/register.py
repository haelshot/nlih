from ninja import Router

from app.schema import RegisterDoctorSchema, RegisterPatientSchema, ResponseSchema
from ninja import Router
from ninja.responses import Response
from app.models import Doctor, Patient, User

router = Router()


@router.post("signup/patient", tags=["Authentication"], response=ResponseSchema)
def patient_signup(request, payload: RegisterPatientSchema):
    try:
        if User.objects.filter(email=payload.email).exists():
            return Response(ResponseSchema(is_ok=False, message="Email already exists.", payload=None, err_data=None), status=409)

        user = User.objects.create_user(
            email=payload.email.lower().strip(),
            password=payload.password,
            first_name=payload.patient_firstname,
            last_name=payload.patient_lastname,
        )

        patient = Patient.objects.create(
            user=user,
            name=user.username,
        )

        payload = {
            "user_id": str(user.id),
            "patient_id": str(patient.id),
            "user_name": payload.patient_name,
            "email": payload.email,
        }
        
        return Response(
            ResponseSchema(
                is_ok=True,
                message='user registered successfully',
                payload=payload,
                err_data=None
            ),
            status=200
        )
    except Exception as e:
        return Response(
            data={"error": {"name": "SIGNUP_ERROR", "details": f"An error occurred during signup, {e}"}},
            status=500
        )
    

@router.post("signup/doctor", tags=["Authentication"], response=ResponseSchema)
def doctor_signup(request, payload: RegisterDoctorSchema):
    try:
        if User.objects.filter(email=payload.email).exists():
            return Response(ResponseSchema(is_ok=False, message="Email already exists.", payload=None, err_data=None), status=409)

        user = User.objects.create_user(
            email=payload.email.lower().strip(),
            password=payload.password,
            first_name=payload.doctor_firstname,
            last_name=payload.doctor_lastname,
        )

        doctor = Doctor.objects.create(
            user=user,
            name=user.username,
        )
        
        payload = {
            "user_id": str(user.id),
            "doctor_id": str(doctor.id),
            "user_name": payload.doctor_name,
            "email": payload.email,
        }
        
        return Response(
            ResponseSchema(
                is_ok=True,
                message='user registered successfully',
                payload=payload,
                err_data=None
            ),
            status=200
        )
    except Exception as e:
        return Response(
            data={"error": {"name": "SIGNUP_ERROR", "details": f"An error occurred during signup, {e}"}},
            status=500
        )