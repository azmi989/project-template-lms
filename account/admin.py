from django.contrib import admin

from .models import (
    User as MyUser,
    Profession,
    Skills
)

admin.site.register(Skills)
admin.site.register(Profession)
admin.site.register(MyUser)
