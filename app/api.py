from datetime import datetime
from ninja import Router

from app.models import User
from nlih.settings import DEPLOYMENT_TIER

router = Router()


if DEPLOYMENT_TIER == "local":
    @router.get("/status/")
    def check_db(request):
        try:
            property_count = User.objects.all().count()
            response_data = {"status": "ok1 local server"}
        except Exception as e:
            response_data = {"status": "ok2"}
        return response_data

elif DEPLOYMENT_TIER == "dev":
    @router.get("/status/")
    def check_db(request):
        try:
            property_count = User.objects.all().count()
            response_data = {"status": "ok1 dev server"}
        except Exception as e:
            response_data = {"status": "ok2"}
        return response_data