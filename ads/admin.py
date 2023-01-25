from django.contrib import admin
from .models import Location, User, Ad, Category

# Register your models here.
admin.site.register(Location)
admin.site.register(User)
admin.site.register(Ad)
admin.site.register(Category)