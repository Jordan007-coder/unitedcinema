from django.contrib import admin
from .models import Film, WeeklySchedule, Package, WeekendPackage, PackageCategory

admin.site.register(Film)
admin.site.register(WeeklySchedule)
admin.site.register(PackageCategory)
admin.site.register(Package)
admin.site.register(WeekendPackage)

