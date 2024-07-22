from ninja import NinjaAPI
from app.api import router as api_router
from app.controllers.authentication.register import router as signup_handler
from app.controllers.authentication.signin import router as signin_handler
from app.controllers.appointments.appointments import router as appointment_router
from ninja_jwt.controller import NinjaJWTDefaultController

api = NinjaAPI()

api.add_router("/v1/", api_router)
api.add_router("/v1/", signup_handler)
api.add_router("/v1/", signin_handler)
api.add_router("/v1/", appointment_router)

api.register_controllers(NinjaJWTDefaultController)
