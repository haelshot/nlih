from django.contrib import admin
from app.models import *


admin.site.register(User)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Appointments)

# Register your models here.
