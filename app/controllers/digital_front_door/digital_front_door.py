from typing import List
from django.shortcuts import get_object_or_404
from ninja import Router
from app.models import AnonymousAppointment, AnonymousUser, Estimate, Service
from app.schema import AnonymousAppointmentSchema, ServiceSchema, EstimateSchema, AppointmentCreateSchema, ResponseSchema

router = Router()

@router.get("/services", response=List[ServiceSchema], tags=["Digital Front Door"])
def list_services(request):
    services = Service.objects.all()
    return services



@router.get("/services/{service_id}/estimates", response=List[EstimateSchema], tags=["Digital Front Door"])
def get_estimates(request, service_id: str):
    estimates = Estimate.objects.filter(service_id=service_id)
    return estimates


@router.post("anonymous/appointments/schedule", response=ResponseSchema, tags=["Digital Front Door"])
def schedule_anonymous_appointment(request, data: AppointmentCreateSchema):
    session_id = data.session_id
    anonymous_user, created = AnonymousUser.objects.get_or_create(session_id=session_id)
    
    appointment = AnonymousAppointment.objects.create(
        anonymous_user=anonymous_user,
        service_id=data.service_id,
        appointment_time=data.appointment_time,
        contact_info=data.contact_info,
        status="scheduled"
    )
    
    payload = {
        "appointment_id": appointment.id,
        "status": appointment.status
    }
    
    return ResponseSchema(
        is_ok=True,
        message="Appointment scheduled successfully",
        payload=payload,
        err_data=None
    )

@router.get("/appointments", response=List[AnonymousAppointmentSchema], tags=["Digital Front Door"])
def list_appointments(request, session_id: str):
    anonymous_user = get_object_or_404(AnonymousUser, session_id=session_id)
    appointments = AnonymousAppointment.objects.filter(anonymous_user=anonymous_user)
    return appointments


@router.post("/appointments/cancel", response=ResponseSchema, tags=["Digital Front Door"])
def cancel_appointment(request, appointment_id: str, session_id: str):
    anonymous_user = get_object_or_404(AnonymousUser, session_id=session_id)
    appointment = get_object_or_404(AnonymousAppointment, id=appointment_id, anonymous_user=anonymous_user)
    
    if appointment.status != "scheduled":
        return ResponseSchema(
            is_ok=False,
            message="Cannot cancel a non-scheduled appointment",
            payload=None,
            err_data="Invalid appointment status"
        )
    
    appointment.status = "cancelled"
    appointment.save()
    
    return ResponseSchema(
        is_ok=True,
        message="Appointment cancelled successfully",
        payload={"appointment_id": appointment.id},
        err_data=None
    )
