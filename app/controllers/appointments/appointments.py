from datetime import datetime
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja_jwt.authentication import JWTAuth
from ninja.responses import Response
from app.models import Appointments, Doctor, Patient
from app.schema import AppointmentSchema, ResponseSchema

router = Router()

@router.get("appointment/available_doctors", auth=JWTAuth(), tags=["Appointments"])
def get_all_available_doctors(request):
    user = request.auth
    if not user:
        return Response(
            ResponseSchema(
                is_ok=False,
                message="User not authenticated",
                payload=None,
                err_data=None
            ),
            status=403
        )
    
    doctors = Doctor.objects.filter(is_free=True).values('id','name', 'is_free')
    payload = {
        "doctors": list(doctors)
    }
    return Response(
        ResponseSchema(
            is_ok=True,
            message="Available doctors retrieved successfully",
            payload=payload,
            err_data=None
        )
    )


@router.post("appointment/book",auth=JWTAuth(), response=ResponseSchema, tags=["Appointments"])
def book_an_appointment(request, appointment: AppointmentSchema):
    user = request.user
    if not user:
        return ResponseSchema(
            is_ok=False,
            message="User not authenticated",
            payload=None,
            err_data="Authentication required"
        )

    doctor = get_object_or_404(Doctor, id=appointment.doctor_id)
    if not doctor.is_free:
        return ResponseSchema(
            is_ok=False,
            message="Doctor not available at the specified time",
            payload=None,
            err_data="Doctor is busy or invalid time provided"
        )
    
    patient = Patient.objects.get(user_id=user.id)

    new_appointment = Appointments.objects.create(
        patient=patient,  
        doctor=doctor,
        status="scheduled",
        booking_time=appointment.datetime
    )

    doctor.is_free = False
    doctor.save()

    payload = {
        "appointment_id": new_appointment.id,
        "time": appointment.datetime
        }
    
    return ResponseSchema(
        is_ok=True,
        message="Appointment booked successfully",
        payload=payload,
        err_data=None
    )

@router.post("appointment/is_accepted", auth=JWTAuth(), tags=["Appointments"])
def accept_or_reject_appointment(request, appointment_id: str, is_accepted: bool):
    user = request.user
    doctor = Doctor.objects.get(user_id=user.id)

    if not user or not doctor:
        return ResponseSchema(
            is_ok=False,
            message="User not authenticated",
            payload=None,
            err_data="Authentication required"
        )
    try:
        appointment = Appointments.objects.get(id=appointment_id)
    except Exception as e:
        return ResponseSchema(
            is_ok=False,
            message="Appointment does not exist",
            payload=None,
            err_data=e
        )
    if is_accepted:
        appointment.status = "checked-in"
        appointment.save()
        print(f"status: {appointment.status}")
        return ResponseSchema(
            is_ok=True,
            message="Appointment checked-in",
            payload=None,
            err_data=None
        )
    
    else:
        appointment.status = "rejected"
        appointment.save()
        return ResponseSchema(
            is_ok=True,
            message="Appointment rejected",
            payload=None,
            err_data=None
        )



        

@router.post("appointment/is_completed", auth=JWTAuth(), tags=["Appointments"])
def mark_appointment_as_completed(request, appointment_id: str):
    user = request.user
    doctor = Doctor.objects.get(user_id=user.id)

    if not user or not doctor:
        return ResponseSchema(
            is_ok=False,
            message="User not authenticated",
            payload=None,
            err_data="Authentication required"
        )
    
    try:
        appointment = Appointments.objects.get(id=appointment_id)
    except Exception as e:
        return ResponseSchema(
            is_ok=False,
            message="Appointment does not exist",
            payload=None,
            err_data=e
        )
    appointment.status = "completed"
    doctor.is_free = True

    appointment.save()
    doctor.save()

    return ResponseSchema(
        is_ok=True,
        message="Appointment completed",
        payload=None,
        err_data=None
    )


@router.get("appointment/all_appointments", auth=JWTAuth(), tags=["Appointments"])
def all_appointments_for_doctor(request):
    user = request.user
    doctor = Doctor.objects.get(user_id=user.id)

    if not user or not doctor:
        return ResponseSchema(
            is_ok=False,
            message="User not authenticated",
            payload=None,
            err_data="Authentication required"
        )
    
    appointment = Appointments.objects.all().values('id','patient__name','status', 'doctor__name', 'booking_time')
    payload = {
        "appointment": list(appointment)
    }
    return Response(
        ResponseSchema(
            is_ok=True,
            message="Available appointment retrieved successfully",
            payload=payload,
            err_data=None
        )
    )


@router.post("/appointment/cancel", auth=JWTAuth(), tags=["Appointments"])
def cancel_appointment(request, appointment_id: str):
    user = request.user
    if not user:
        return ResponseSchema(
            is_ok=False,
            message="User not authenticated",
            payload=None,
            err_data="Authentication required"
        )

    try:
        appointment = Appointments.objects.get(id=appointment_id, patient__user_id=user.id)
        appointment.status = "cancelled"
        appointment.save()
        appointment.doctor.is_free = True
        appointment.doctor.save()
        return ResponseSchema(
            is_ok=True,
            message="Appointment cancelled successfully",
            payload=None,
            err_data=None
        )
    except Exception as e:
        return ResponseSchema(
            is_ok=False,
            message="Appointment not found or not owned by user",
            payload=None,
            err_data=str(e)
        )


@router.post("/appointment/reschedule", auth=JWTAuth(), tags=["Appointments"])
def reschedule_appointment(request, appointment_id: str, new_datetime: datetime):
    user = request.user
    if not user:
        return ResponseSchema(
            is_ok=False,
            message="User not authenticated",
            payload=None,
            err_data="Authentication required"
        )

    try:
        appointment = Appointments.objects.get(id=appointment_id, patient__user_id=user.id)
        if appointment.status != "completed":
            appointment.status = "scheduled"
            appointment.booking_time = new_datetime
            appointment.save()
            return ResponseSchema(
                is_ok=True,
                message="Appointment rescheduled successfully",
                payload=None,
                err_data=None
            )
        else:
            return ResponseSchema(
                is_ok=False,
                message="Cannot reschedule a completed appointment",
                payload=None,
                err_data=None
            )
    except Exception as e:
        return ResponseSchema(
            is_ok=False,
            message="Appointment not found or not owned by user",
            payload=None,
            err_data=str(e)
        )


